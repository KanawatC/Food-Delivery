"""First-Order Reactivation Trigger.

Problem: 66% of customers have placed exactly one order, ever. This script sizes
the stalled one-time-buyer population, tiers them by first-order value, sizes a
break-even-justified reactivation offer per tier, and exports a ranked target
list for outreach.

Reads final_cleaned_data.csv, writes reactivation_target_list.csv and
reactivation_gap_analysis.png.
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings('ignore')

# Trigger: operational point to reach out (between median 17d and P75 41d observed reorder gap)
TRIGGER_DAYS = 30

# Stall cutoff: classification threshold for "genuinely stalled" one-time customers.
# 60 days is a reasonably conservative cutoff (most, though not all, organic reordering has
# concluded by then); a stricter 90-day cutoff is checked below as a sensitivity check.
STALL_CUTOFF_DAYS = 60

# Per-tier caps derived from each tier's own value range (~20% of the tier's upper boundary,
# rounded), so the offer stays proportionate without letting the High tier's long right tail
# (first-order values up to ~12,663) produce a runaway discount.
TIER_CAPS = {'Low': 75, 'Mid': 140, 'High': 250}


def load_reorder_gaps(path='final_cleaned_data.csv'):
    df = pd.read_csv(path)
    df['Order Placed At'] = pd.to_datetime(df['Order Placed At'], errors='coerce')
    df = df.dropna(subset=['Order Placed At', 'Customer ID'])
    df = df.sort_values(['Customer ID', 'Order Placed At'])
    df['order_seq'] = df.groupby('Customer ID').cumcount() + 1

    max_date = df['Order Placed At'].max()

    first = (df[df['order_seq'] == 1][['Customer ID', 'Order Placed At', 'Total']]
             .rename(columns={'Order Placed At': 'first_date', 'Total': 'first_value'}))
    second = (df[df['order_seq'] == 2][['Customer ID', 'Order Placed At']]
              .rename(columns={'Order Placed At': 'second_date'}))

    reorder = first.merge(second, on='Customer ID', how='left')
    reorder['gap_days'] = (reorder['second_date'] - reorder['first_date']).dt.days
    reorder['days_since_first'] = (max_date - reorder['first_date']).dt.days
    return reorder


def recommended_offer(row):
    return round(min(0.20 * row['first_value'], TIER_CAPS[row['value_tier']]), 2)


def main():
    reorder = load_reorder_gaps()

    print("--- Days between 1st and 2nd order (customers who reordered) ---")
    print(reorder.dropna(subset=['second_date'])['gap_days'].describe(percentiles=[.1, .25, .5, .75, .9]))

    onetime = reorder[reorder['second_date'].isna()].copy()
    eligible = onetime[onetime['days_since_first'] >= STALL_CUTOFF_DAYS].copy()

    print(f"\nEligible stalled one-time customers (>= {STALL_CUTOFF_DAYS} days since first order): {len(eligible):,}")
    print(f"Total stalled first-order GMV: {eligible['first_value'].sum():,.2f}")

    strict = onetime[onetime['days_since_first'] >= 90]
    print(f"Sensitivity check (>= 90 days): {len(strict):,} customers, GMV {strict['first_value'].sum():,.2f}")

    eligible['value_tier'] = pd.qcut(eligible['first_value'], q=3, labels=['Low', 'Mid', 'High'])
    print("\n--- Value tiers among eligible stalled customers ---")
    print(eligible.groupby('value_tier')['first_value'].agg(['count', 'mean', 'min', 'max', 'sum']))

    eligible['recommended_offer'] = eligible.apply(recommended_offer, axis=1)
    print("\n--- Recommended offer by tier ---")
    print(eligible.groupby('value_tier')['recommended_offer'].agg(['mean', 'max', 'sum']))

    baseline_reorder_rate = reorder['second_date'].notna().mean() * 100

    summary = eligible.groupby('value_tier').agg(
        n=('Customer ID', 'count'),
        mean_first_value=('first_value', 'mean'),
        total_campaign_cost=('recommended_offer', 'sum')
    ).reset_index()
    summary['required_reorders_to_break_even'] = summary['total_campaign_cost'] / summary['mean_first_value']
    summary['required_reorder_rate_pct'] = summary['required_reorders_to_break_even'] / summary['n'] * 100

    print(f"\nPlatform's observed baseline reorder rate: {baseline_reorder_rate:.1f}%\n")
    print(summary.to_string(index=False, formatters={
        'mean_first_value': '{:,.2f}'.format,
        'total_campaign_cost': '{:,.2f}'.format,
        'required_reorders_to_break_even': '{:,.1f}'.format,
        'required_reorder_rate_pct': '{:.1f}%'.format,
    }))

    plt.rcParams.update(plt.rcParamsDefault)
    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    reordered_gaps = reorder.dropna(subset=['second_date'])['gap_days']

    sns.histplot(reordered_gaps, bins=40, color='royalblue', ax=axes[0])
    axes[0].axvline(TRIGGER_DAYS, color='crimson', linestyle='--', linewidth=2, label=f'Trigger: {TRIGGER_DAYS} days')
    axes[0].set_title('Distribution of Days to 2nd Order', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Days Between 1st and 2nd Order')
    axes[0].legend()

    sns.ecdfplot(reordered_gaps, ax=axes[1], color='royalblue', linewidth=2)
    axes[1].axvline(TRIGGER_DAYS, color='crimson', linestyle='--', linewidth=2, label=f'Trigger: {TRIGGER_DAYS} days')
    axes[1].set_title('ECDF: Days to 2nd Order', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Days Between 1st and 2nd Order')
    axes[1].set_ylabel('Cumulative Proportion of Reordering Customers')
    axes[1].legend()

    plt.tight_layout()
    plt.savefig('reactivation_gap_analysis.png', dpi=150)
    print("\nSaved chart to 'reactivation_gap_analysis.png'")

    output = eligible[['Customer ID', 'first_date', 'first_value', 'days_since_first', 'value_tier', 'recommended_offer']].copy()
    output = output.rename(columns={'days_since_first': 'days_since_first_order'})
    output = output.sort_values('first_value', ascending=False)

    output.to_csv('reactivation_target_list.csv', index=False)
    print(f"Saved {len(output):,} target customers to 'reactivation_target_list.csv'")
    print(output.head().to_string(index=False))


if __name__ == '__main__':
    main()
