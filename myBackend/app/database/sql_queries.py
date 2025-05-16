# Transaction-related queries
CREATE_TRANSACTION = """
    INSERT INTO transactions (amount, description, date, account_id, category_id, user_id, currency_id)
    VALUES ($1, $2, $3, $4, $5, $6, $7)
    RETURNING transaction_id;
"""

UPDATE_ACCOUNT_BALANCE = """
    UPDATE accounts
    SET balance = balance + $1
    FROM currency
    WHERE accounts.account_id = $2 
      AND accounts.user_id = $3 
      AND accounts.currency_id = $4
    RETURNING accounts.account_id;
"""


# user related queries
CREATE_USER = """
        INSERT INTO users (email, first_name, last_name, password_hash, phone_number, dob, phone_verified)
        VALUES ($1, $2, $3, $4, $5, $6, FALSE)
        RETURNING user_id;
    """

LOGIN_QUERY = """
        SELECT user_id, email, password_hash FROM users
        WHERE email = $1;
    """

GET_USER_QUERY = """
        SELECT user_id, email, first_name, last_name
        FROM users
        WHERE user_id = $1;
    """

GET_TRANSACTIONS_BY_USER = """
        SELECT transaction_id, account_id, currency_id, category_id, amount, description, created_at
        FROM transactions t
        JOIN accounts a ON t.account_id = a.account_id
        WHERE a.user_id = $1
        ORDER BY created_at DESC;
    """