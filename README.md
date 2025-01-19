# Second-Price Auction Algorithm: Strategic Bidding Framework

## **Overview**
This project focuses on implementing a competitive bidding algorithm for a second-price auction used in online advertising **from scratch**. The auction design incentivizes truthful bidding by charging the winning bidder the second-highest bid. The challenge involved creating a `Bidder` class that efficiently balances exploration (learning user behavior) and exploitation (maximizing payoffs) in a competitive landscape.

Note: This project models a simplified version of second-price auctions, emphasizing strategic algorithm design without the use of machine learning techniques, offering a foundation for deeper exploration of auction dynamics.

## **Auction Structure**
The auction consists of multiple rounds involving a set of users and bidders:
- **Users:** Each user has a fixed click probability, randomly assigned from a uniform distribution [0, 1]. Users are randomly selected each round.
- **Bidders:** Compete to display ads to users by submitting sealed bids. The objective is to maximize the ending balance.
- **Winning Criteria:** The bidder with the highest bid wins, paying the second-highest bid amount.

### Auction Flow:
1. A user is randomly chosen, and bidders place their bids.
2. The highest bid determines the winner.
3. The winning bidder’s balance is updated based on the auction outcome:
   - If the user clicks the ad, the winner earns \$1.
   - Regardless of clicks, the balance decreases by the second-highest bid amount.
4. Non-winning bidders are informed of the winning bid.

## **Implementation**
The project comprises three main components: 

### **1. User Class**
Simulates user behavior, including:
- Assigning a unique click probability to each user.
- Returning whether a user clicked an ad based on their click probability.

### **2. Bidder Class**
Implements a dynamic strategy for competing in the auction:
- Balances exploration and exploitation through historical data analysis.
- Adapts bid amounts based on user behavior and competitor bids.
- Tracks performance metrics to refine strategies over time.

### **3. Auction Class**
Manages the auction process and provides insights through visualization:
- Conducts the auction, including selecting users, collecting bids, and determining outcomes.
- Maintains bidder balances and logs performance data.
- Offers a `plot_history()` method to visualize bidder performance over time.

## **Features**
- **Dynamic Bidding Strategy:** The bidding algorithm adapts based on observed click probabilities and competitor behaviors.
- **Visualization:** A comprehensive performance visualization to evaluate bidder strategies.
- **Object-Oriented Design:** Flexible and modular code structure, enabling easy scalability.

## **Technologies Used**
- **Python Libraries:** 
  - `numpy` for numerical operations.
  - `matplotlib` and `seaborn` for visualizations.
  - `pandas` for data manipulation.
  
## **Visualization Example**
The project includes a graphical representation of bidder balances over time. This visualization helps assess the effectiveness of different strategies.

## **Key Takeaways**
- Developed a dynamic strategy for second-price auction bidding.
- Enhanced proficiency in Python and its data science libraries.
- Gained experience in modeling competitive environments with strategic interactions.
- Successfully balanced exploration and exploitation to optimize outcomes.

## **Results**
- Outperformed baseline strategies in simulations.
- Achieved competitive performance in a multi-bidder environment.

## **Further Exploration**
- Extend strategies to account for contextual targeting in ad auctions.
- Explore reinforcement learning for real-time optimization in auction scenarios.

## **Repository Structure**
- `auction.py`: Contains the `User` and `Auction` class implementations.
- `bidder.py`: Contains the `Bidder` class with a dynamic bidding algorithm.
- `simulate_auction.py`: Script to simulate auctions with multiple strategies.

---

Created this for a class project. Once all submissions were collected, my algorithm submission `bidder_naidoo.py` was pit against all other submissions in a final competition. In a competition game, one Bidder from each submissions will be created along with a set of Users. Points were awarded based on the final ranking. `This placed Top 10 out of 130 submissions`.