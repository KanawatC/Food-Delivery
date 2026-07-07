# Food-Delivery
## 🛒 Customer Behavior
<img width="1001" height="557" alt="image" src="https://github.com/user-attachments/assets/8d870da1-9d60-4e36-acb8-9fbcb39c0290" />

## 📊 Customer Segmentation (RFM Analysis)

We applied RFM (Recency, Frequency, Monetary) analysis to segment our customer base and understand purchasing behaviors.

**Customer Distribution by Segment:**
* Need Attention: 4,427 users
* Potential Loyalist: 3,473 users
* Loyal Customers: 2,606 users
* VIP / Champions: 1,098 users
* At Risk: 3 users

**Key Insights:**
* **High-Value Champions:** Our 1,098 VIP/Champions have exceptionally high 'Monetary' scores and drive a disproportionately large share of total revenue. Retaining them through exclusive loyalty programs remains critical.
* **The real churn problem is first-order stall, not lapsed VIPs:** True 'At Risk' (customers who ordered repeatedly and have since gone quiet) is only 3 users — the platform doesn't have a lapsed-repeat-customer problem. Instead, 66% of all customers (7,713 of 11,607) have placed exactly one order, ever, and ~4,835 of them have gone well past their natural reorder window without a second order (~3.25M in stalled first-order GMV). See the "First-Order Reactivation" section below for the problem breakdown and the targeting program built to address it.

## 🎯 First-Order Reactivation: Problem, Solution & Results

### Problem

While validating the RFM segmentation, we found the original 'At Risk' segment (267 users) was a scoring artifact, not a real signal — a frequency-scoring bug was mislabeling one-time buyers as lapsed repeat customers. Fixing it (see RFM section above) exposed the platform's actual churn problem:

* **66% of all customers (7,713 of 11,607) have placed exactly one order, ever.**
* After excluding customers who simply haven't had enough time yet to reorder (first order less than 60 days before the end of the data window), **4,835 customers are genuinely stalled after a single order — representing 3,254,932.38 in first-order GMV that never repeated.**
* Among the 3,894 customers who *did* reorder, the gap to their 2nd order has a median of 17 days and a 75th percentile of 41 days — most organic reordering happens within about six weeks, after which it drops off sharply.

### Solution

We built a data-driven **"First-Order Reactivation Trigger"** (implemented in `Food_Delivery.ipynb`):

1. **Trigger rule:** flag a first-time customer for a reactivation nudge if no 2nd order has landed within **30 days** (between the observed median of 17 days and the 75th percentile of 41 days).
2. **Value-tiered offer:** split eligible customers into value terciles (Low / Mid / High by first-order value) and offer 20% off, capped at 75 / 140 / 250 per tier respectively — directionally supported by the platform's own proven promo elasticity (discounts already drive +57% order volume / +47% revenue platform-wide — see Promotion Strategy section below).
3. **Break-even check:** for each tier, state the reorder rate required for the campaign to pay for its own cost, and compare it against the platform's already-observed baseline reorder rate — a plausibility check, not an assumed conversion rate.
4. **Deliverable:** an exported, ranked target list (`reactivation_target_list.csv`) that an outreach/marketing team can act on directly, highest-value stalled customers first.

### Results (from running the notebook)

| Value Tier | Customers | Avg. First Order | Total Campaign Cost | Required Reorder Rate to Break Even |
| :--- | :--- | :--- | :--- | :--- |
| Low | 1,633 | 310.82 | 97,438.02 | ~19.2% |
| Mid | 1,597 | 588.67 | 187,954.08 | ~20.0% |
| High | 1,605 | 1,126.02 | 320,468.42 | ~17.7% |

* **All three tiers require only ~18–20% of stalled customers to reorder once to break even** — comfortably below the platform's already-observed baseline reorder rate of **33.5%**, suggesting the campaign is plausible rather than speculative.
* Total addressable opportunity: **4,835 target customers**, **3,254,932.38** in stalled first-order GMV, **605,860.52** total campaign cost across all tiers if every eligible customer is reached.
* Full ranked list exported to [`reactivation_target_list.csv`](reactivation_target_list.csv) (Customer ID, first order date/value, days since first order, value tier, recommended offer).

## 🏆 Top Performing Restaurants

An analysis of vendor performance reveals a significant concentration of revenue among a few key players. 

**Top 5 Vendors by Revenue:**
| Restaurant Name | Total Revenue | Total Orders | Average Order Value (AOV) |
| :--- | :--- | :--- | :--- |
| Aura Pizzas | 10,751,617.42 | 14,548 | 739.04 |
| Swaad | 3,545,521.86 | 6,332 | 559.94 |
| Tandoori Junction | 133,665.95 | 154 | 867.96 |
| Dilli Burger Adda | 101,709.62 | 227 | 448.06 |
| The Chicken Junction | 12,380.99 | 32 | 386.91 |

**Key Insights:**
* **Market Dominance:** 'Aura Pizzas' is the undisputed market leader, generating over 10M in revenue and handling more than double the order volume of the second-place vendor. 
* **High Platform Dependency:** The platform's revenue is heavily reliant on the top 2 vendors. This presents a business risk if these vendors were to churn.
* **Actionable Strategy:** The business development team should focus on diversifying platform offerings and running targeted campaigns to boost mid-tier restaurants (like Tandoori Junction and Dilli Burger Adda) to balance the revenue distribution.

## 📈 Promotion Strategy & Impact

To evaluate the effectiveness of the platform's discount strategy, we compared orders with and without promotional codes.

**Performance Summary:**
| Has Discount | Total Orders | Total Revenue | Average Order Value (AOV) |
| :--- | :--- | :--- | :--- |
| No Discount | 8,292 | 5,890,214.27 | 710.35 |
| With Discount | 13,029 | 8,663,843.87 | 664.97 |

**Key Insights:**
* **Volume Drives Revenue:** Offering discounts is a highly effective strategy for this platform. While promotions slightly decrease the Average Order Value (from 710.35 to 664.97), they drive a massive 57% increase in order volume.
* **Revenue Maximization:** The surge in transaction volume completely offsets the lower margin per order, resulting in a 47% boost in Total Revenue when discounts are applied.
* **Pricing Elasticity:** Customers on this platform are highly price-sensitive. Promotional campaigns are the primary catalyst for driving user engagement and accelerating platform growth.
