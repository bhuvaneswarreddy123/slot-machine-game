import streamlit as st
import random

MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLS = 3

symbol_count = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8
}

symbol_value = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2
}

def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)

    columns = []
    for _ in range(cols):
        col = []
        current_symbols = all_symbols[:]
        for row in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            col.append(value)
        columns.append(col)
    return columns

def print_slot_machine(columns):
    slot_machine = ""
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i != len(columns) - 1:
                slot_machine += column[row] + " | "
            else:
                slot_machine += column[row]
        slot_machine += "\n"
    return slot_machine

def check_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
        else:
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)
    return winnings, winning_lines

def main():
    st.title('Slot Machine Game')
    
    # User input for deposit
    balance = st.number_input("Deposit Amount:", min_value=0, step=1, key="deposit_amount")
    
    if balance <= 0:
        st.warning("Please deposit a positive amount.")
        return
    
    # Initialize session state variables
    if 'balance' not in st.session_state:
        st.session_state.balance = balance
    if 'slots' not in st.session_state:
        st.session_state.slots = []
    if 'winnings' not in st.session_state:
        st.session_state.winnings = 0
    if 'winning_lines' not in st.session_state:
        st.session_state.winning_lines = []

    # Display current balance
    st.write(f"Current Balance: ${st.session_state.balance}")
    
    # User input for number of lines
    lines = st.slider("Number of Lines to Bet On", 1, MAX_LINES, 1, key="lines_slider")
    
    # User input for bet per line
    bet = st.slider(f"Bet Per Line (Min: ${MIN_BET}, Max: ${MAX_BET})", MIN_BET, MAX_BET, MIN_BET, key="bet_slider")
    
    # Button to perform spin
    if st.button("Spin", key="spin"):
        total_bet = lines * bet
        if total_bet > st.session_state.balance:
            st.warning(f"Not enough balance. Your current balance is ${st.session_state.balance}.")
        else:
            st.session_state.balance -= total_bet
            st.write(f"You are betting ${bet} on {lines} lines. Total bet is ${total_bet}.")
            
            # Generate slot machine spin and display it
            st.session_state.slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
            slot_machine = print_slot_machine(st.session_state.slots)
            st.text(slot_machine)
            
            # Calculate winnings
            st.session_state.winnings, st.session_state.winning_lines = check_winnings(st.session_state.slots, lines, bet, symbol_value)
            st.session_state.balance += st.session_state.winnings
            
            st.write(f"You won ${st.session_state.winnings}.")
            st.write(f"You won on lines: {', '.join(map(str, st.session_state.winning_lines))}")
            st.write(f"New Balance: ${st.session_state.balance}")
    
    # Show game over message if balance is zero or less
    if st.session_state.balance <= 0:
        st.write("Game Over. You ran out of money.")
    
if __name__ == "__main__":
    main()
