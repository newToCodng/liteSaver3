class Transaction {
  final int accountId;
  final int categoryId;
  final double amount;
  final String description;

  Transaction({
    required this.accountId,
    required this.categoryId,
    required this.amount,
    required this.description,
  });

  factory Transaction.fromJson(Map<String, dynamic> json) => Transaction(
    accountId: json['account_id'],
    categoryId: json['category_id'],
    amount: json['amount'].toDouble(),
    description: json['description'],
  );
}