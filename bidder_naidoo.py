import numpy as np

class Bidder:
    """Bidder Class for the Auction"""
    _instance_count = 1

    def __init__(self, num_users, num_rounds):
        self.bidder_id = Bidder._instance_count
        Bidder._instance_count += 1
        self.num_users = num_users
        self.num_rounds = num_rounds
        self.round_number = 1
        self.approx_train_rounds_per_user = round((self.num_rounds / self.num_users) / 3, 0)
        self.bidder_budget = 0
        self.usr_clickrate_dict = {}
        self.user_aggregate_click_dict = {}
        self.final_bid = 0
        self.log = np.array([])
        self.personal_bid_pattern = np.array([[self.round_number, None, None, None, self.bidder_budget]])

    def __repr__(self):
        return f"b{self.bidder_id}"

    def __str__(self):
        return f"b{self.bidder_id}"

    def calculate_expected_value(self, second_price_bid, est_click_rate):
        """Return expected value of a bid given the click rate."""
        return est_click_rate * (1 - second_price_bid) + (1 - est_click_rate) * (0 - second_price_bid)

    def bid_price(self, expected_val, click_rate):
        """Return bid price of a given expected value """
        return click_rate - expected_val

    def calculate_expected_val_last_n_bids(self, num_bid_lookback, user_id, user_log, est_click_rate):
        """Calculate the expected_val with respect to the last N winning bids on a given user."""
        user_log = user_log[user_log[:, 0] == user_id]
        count_last_n_bids = 0 - num_bid_lookback
        mean = user_log[:, 2][count_last_n_bids:].mean()
        return mean, self.calculate_expected_value(mean, est_click_rate)

    def submit_expected_val_bid_price(self, user_id, est_click_rate, log):
        """Submit a bid price based on the expected_val"""
        last10, last10_expected_val = self.calculate_expected_val_last_n_bids(10, user_id, log, est_click_rate)
        _, last3_expected_val = self.calculate_expected_val_last_n_bids(3, user_id, log, est_click_rate)

        if last10_expected_val < 0:
            self.final_bid = 0.0001
        else:
            if last3_expected_val < 0:
                self.final_bid = 0.0001
            else:
                self.final_bid = (last10 + 0.00001) * 5

        return self.final_bid

    def update_dict(self, user, final_bid, bidder_log):
        """Use the bidder log to update the click rate dictionary."""
        if final_bid is None:
            return 0

        user_log = bidder_log[bidder_log[:, 0] == user]
        if len(user_log) == 0:
            return 0

        last_record = user_log[-1]
        _, user_won, _, user_clicked = last_record

        self.usr_clickrate_dict[user]["total_rounds"] += 1
        if user_won:
            self.usr_clickrate_dict[user]["total_wins"] += 1
        if user_clicked:
            self.usr_clickrate_dict[user]["total_clicks"] += 1

        bid_modifier = 1 if user_clicked else 0
        self.bidder_budget += (bid_modifier - final_bid)

        if self.usr_clickrate_dict[user]["total_wins"] > 0:
            self.user_aggregate_click_dict[user] = self.usr_clickrate_dict[user]["total_clicks"] / self.usr_clickrate_dict[user]["total_wins"]
        else:
            self.user_aggregate_click_dict[user] = 0

    def aggressive_bid(self, user_id, bidder_log):
        """Use aggressive bidding method"""
        if self.approx_train_rounds_per_user >= 10:
            if user_id not in self.usr_clickrate_dict:
                self.usr_clickrate_dict[user_id] = {
                    "approx_rounds_left": 10,
                    "total_rounds": 0,
                    "total_wins": 0,
                    "total_clicks": 0
                }
                self.user_aggregate_click_dict[user_id] = 0
                self.final_bid = 1
            elif self.usr_clickrate_dict[user_id]["approx_rounds_left"] > 0:
                user_log = bidder_log[bidder_log[:, 0] == user_id]
                last_record = user_log[-1, :]
                self.usr_clickrate_dict[user_id]["approx_rounds_left"] -= 1
                self.final_bid = max(last_record[2] * 2, 1)
            else:
                self.final_bid = 0
        else:
            if user_id not in self.usr_clickrate_dict:
                self.usr_clickrate_dict[user_id] = {
                    "approx_rounds_left": self.approx_train_rounds_per_user,
                    "total_rounds": 0,
                    "total_wins": 0,
                    "total_clicks": 0
                }
                self.final_bid = 1
            elif self.usr_clickrate_dict[user_id]["approx_rounds_left"] > 0:
                self.usr_clickrate_dict[user_id]["approx_rounds_left"] -= 1
                user_log = bidder_log[bidder_log[:, 0] == user_id]
                self.final_bid = user_log[-1:, 2] * 2
                return self.final_bid
            else:
                self.final_bid = 0
        return self.final_bid

    def bid(self, user_id):
        """Return Bid to auction."""
        self.user_id = user_id

        if self.user_id not in self.usr_clickrate_dict:
            self.final_bid = self.aggressive_bid(self.user_id, self.log)
            pers_bid_tracking = np.array([self.round_number, self.user_id, 'aggressive', self.final_bid, self.bidder_budget])
            self.personal_bid_pattern = np.vstack((self.personal_bid_pattern, pers_bid_tracking))
            self.round_number += 1
        elif self.user_id in self.usr_clickrate_dict and self.usr_clickrate_dict[self.user_id]["approx_rounds_left"] > 0 and self.bidder_budget >= -20:
            self.final_bid = self.aggressive_bid(self.user_id, self.log)
            pers_bid_tracking = np.array([self.round_number, self.user_id, 'aggressive', self.final_bid, self.bidder_budget])
            self.personal_bid_pattern = np.vstack((self.personal_bid_pattern, pers_bid_tracking))
            self.round_number += 1
        elif self.user_id in self.usr_clickrate_dict and self.usr_clickrate_dict[self.user_id]["approx_rounds_left"] > 7:
            self.final_bid = self.aggressive_bid(self.user_id, self.log)
            pers_bid_tracking = np.array([self.round_number, self.user_id, 'aggressive', self.final_bid, self.bidder_budget])
            self.personal_bid_pattern = np.vstack((self.personal_bid_pattern, pers_bid_tracking))
            self.round_number += 1
        else:
            est_click_rate = self.user_aggregate_click_dict[self.user_id]
            self.final_bid = self.submit_expected_val_bid_price(self.user_id, est_click_rate, self.log)
            pers_bid_tracking = np.array([self.round_number, self.user_id, 'expected_val_bid', self.final_bid, self.bidder_budget])
            self.personal_bid_pattern = np.vstack((self.personal_bid_pattern, pers_bid_tracking))
            self.round_number += 1
        
        return self.final_bid

    def notify(self, auction_winner, price, clicked):
        """Append auction details to internal log."""
        self.auction_winner = auction_winner
        self.price = price
        self.clicked = clicked
        new_entry = np.array([self.user_id, self.auction_winner, self.price, self.clicked])

        if self.log.size == 0:
            self.log = np.array([new_entry])
            self.update_dict(self.user_id, self.final_bid, self.log)
        else:
            self.log = np.vstack((self.log, new_entry))
            self.update_dict(self.user_id, self.final_bid, self.log)
