import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/transaction_model.dart';
import '../service/token_service.dart';

class TransactionService {
  static const String _baseUrl = 'http://127.0.0.1:8000/transactions';

  static Future<List<Transaction>> getTransactions() async {
    final token = await TokenService.getToken();
    final response = await http.get(
      Uri.parse('$_baseUrl/get_transactions'),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json'
      },
    );

    if (response.statusCode == 200) {
      List<dynamic> data = json.decode(response.body);
      return data.map((json) => Transaction.fromJson(json)).toList();
    }
    throw Exception('Failed to load transactions');
  }

  static Future<int> createTransaction(Transaction transaction) async {
    final token = await TokenService.getToken();
    final response = await http.post(
      Uri.parse('$_baseUrl/add_transactions'),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json'
      },
      body: json.encode({
        'account_id': transaction.accountId,
        'category_id': transaction.categoryId,
        'amount': transaction.amount,
        'description': transaction.description,
      }),
    );

    if (response.statusCode == 200) {
      return json.decode(response.body)['transaction_id'];
    }
    throw Exception('Failed to create transaction');
  }
}