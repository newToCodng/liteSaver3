import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/account_model.dart';
import '../service/token_service.dart';

class AccountService {
  static const String _baseUrl = 'http://your-backend/api/accounts';

  static Future<List<Account>> getAccounts() async {
    final token = await TokenService.getToken();
    final response = await http.get(
      Uri.parse(_baseUrl),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json'
      },
    );

    if (response.statusCode == 200) {
      List<dynamic> data = json.decode(response.body);
      return data.map((json) => Account.fromJson(json)).toList();
    }
    throw Exception('Failed to load accounts');
  }

  static Future<int> createAccount(Account account) async {
    final token = await TokenService.getToken();
    final response = await http.post(
      Uri.parse(_baseUrl),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json'
      },
      body: json.encode({
        'currency_id': account.currencyId,
        'name': account.name,
        'balance': account.balance,
        'account_type': account.accountType,
      }),
    );

    if (response.statusCode == 200) {
      return json.decode(response.body)['account_id'];
    }
    throw Exception('Failed to create account');
  }
}