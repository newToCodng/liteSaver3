class Account {
  final int accountId;
  final String name;
  final double balance;
  final String accountType;
  final int currencyId;

  Account({
    required this.accountId,
    required this.name,
    required this.balance,
    required this.accountType,
    required this.currencyId,
  });

  factory Account.fromJson(Map<String, dynamic> json) => Account(
    accountId: json['account_id'],
    name: json['name'],
    balance: json['balance'].toDouble(),
    accountType: json['account_type'],
    currencyId: json['currency_id'],
  );
}