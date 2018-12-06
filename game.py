class Game:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[' '] * width for row in range(height)]
        # self.board_gui = BoardGUI
        self.position_values = self.setup_values()
        self.order = self.generate_order()
        self.board_score = 0

    def __repr__(self):
        pass

    def setup_values(self):
        table = [[3, 4, 5, 7, 5, 4, 3],
                 [4, 6, 8, 10, 8, 6, 4],
                 [5, 8, 11, 13, 11, 8, 5],
                 [5, 8, 11, 13, 11, 8, 5],
                 [4, 6, 8, 10, 8, 6, 4],
                 [3, 4, 5, 7, 5, 4, 3]]
        
        return table

    def generate_order(self):
        order = []
        for i in range(int(self.width / 2) - 1, 0, -1):
            order.append(i)
            order.append(self.width - 1 - i)
        
        if self.width % 2 == 1:
            order.append(int(self.width / 2))

        return order

    def add_token(self, col, player):
        for row in range(self.height - 1, 0, -1):
            if self.board[row][col] == ' ':
                self.board[row][col] = player
                return row, col

    def reset_board(self):
        for row in range(self.height):
            for col in rnage(self.width):
                self.data[row][col] = ' '
    
    def allows_move(self, col):
        return col in range(self.width) and self.data[0][col] == ' '
    
    def is_game_over(self):
        for col in range(self.width):
            if self.allows_move(col):
                return False
            
        return True
    
    def remove_token(self, col):
        if col < 0 or col >= self.width:
            return

        for row in range(self.height):
            if self.board[row][col] != ' ':
                self.board[row][col] = ' '
                return

    def has_won(self, player):
        for row in range(self.height):
            for col in range(self.width):
                if check_winner(row, col, player):
                    return True

        return False

    def check_winner(self, row, col, player):
        if row < 0 or row >= self.height:
            return False
        if col < 0 or col >= self.width:
            return False
        
        board = self.board   # faster access
        found_winner = True

        if row + 3 < self.height:
            for i in range(4):
                if board[row + i][col] != player:
                    found_winner = False
                    break
                
                if found_winner:
                    return True

            found_winner = True
        
        if col + 3 < self.width:
            if row + 3 < self.height:
                for i in range(4):
                    if board[row + i][col + i] != player:
                        found_winner = False
                        break
                    
                if found_winner:
                    return True
            
            found_winner = True

            if row - 3 >= 0:
                for i in range(4):
                    if board[row - i][col + 1] != player:
                        found_winner = False
                        break

                if found_winner:
                    return True

            found_winner = True

            for i in range(4):
                if board[row][col + i] != player:
                    found_winner = False
                    break
                
                if found_winner:
                    return True

        return False

    def possible_winning_columns(self, player):
        winning_columns = []
        
        for row in range(self.width):
            if self.allows_move(row):
                self.add_token(row, player)
                if self.has_won(player):
                    winning_columns.append(row)
                self.remove_token(row)
        
        return winning_columns

    def determine_ai_move(self, player):
        score, col = self.alpha_beta_pruning(self.order[0], 4, -999999, 999999,
                                             self.board_score, player)

        for i in range(1, len(self.order)):
            res, temp_col = self.alpha_beta_pruning(self.order[i], 4,
                                                    -999999, 999999,
                                                    self.board_score, player)
            
            if player == '1':
                if score < res:
                    score = res
                    col = temp_col
            else:
                if score > res:
                    score = res
                    col = temp_col

        return col

    def alpha_beta_pruning(self, col, depth, alpha, beta, score, player):
        if self.has_won('1'):
            return 999998, col
        elif self.has_won('0'):
            return -999998, col
        
        if depth == 0 or self.is_game_over():
            return score, col

        if player == '1':
            max_evaluation = -999999
            column_to_play = -1
            for col in range(self.width):
                if self.allows_move(col):
                    self.add_token(col, player)

                    temp_row = 0
                    while self.board[temp_row][col] == ' ':
                        temp_row += 1
                    
                    curr_pos_val = score + self.position_values[temp_row][col]
                    current_eval = self.alpha_beta_pruning(col, depth - 1,
                                                           alpha, beta,
                                                           curr_pos_val,
                                                           '0')[0]

                    alpha = max(alpha, current_eval)

                    if current_eval > max_evaluation:
                        max_evaluation = current_eval
                        column_to_play = col
                    
                    self.remove_token(col)

                    if beta <= alpha:
                        break

            return max_evaluation, column_to_play

        else:
            min_evalulation = 999999
            column_to_play = -1
            for col in range(self.width):
                if self.allows_move(col):
                    self.add_token(col, player)

                    temp_row = 0
                    while self.board[temp_row][col] == ' ':
                        temp_row += 1

                    curr_pos_val = score - self.position_values[temp_row][col]
                    current_eval = self.alpha_beta_pruning(col, depth - 1,
                                                           alpha, beta,
                                                           curr_pos_val,
                                                           '1')[0]

                    beta = min(beta, current_eval)
                    
                    if min_evalulation > current_eval:
                        min_evalulation = current_eval
                        column_to_play = col

                    self.remove_token(col)

                    if beta <= alpha:
                        break

            return min_evalulation, column_to_play
                    
