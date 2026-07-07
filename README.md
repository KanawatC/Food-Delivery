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
* **The real churn problem is first-order stall, not lapsed VIPs:** True 'At Risk' (customers who ordered repeatedly and have since gone quiet) is only 3 users — the platform doesn't have a lapsed-repeat-customer problem. Instead, 66% of all customers (7,713 of 11,607) have placed exactly one order, ever, and ~4,835 of them have gone well past their natural reorder window without a second order (~₹3.25M in stalled first-order GMV). See the "First-Order Reactivation" section in `Food_Delivery.ipynb` for the targeting program built to address this.

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
