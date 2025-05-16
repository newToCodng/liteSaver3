import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/user_model.dart';
import 'token_service.dart';

class AuthService {
  static const String _baseUrl = 'http://127.0.0.1:8000/users';

  static Future<bool> login(String email, String password) async {
    try {
      final response = await http.post(
        Uri.parse('$_baseUrl/login'),
        body: json.encode({'email': email, 'password': password}),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final token = json.decode(response.body)['access_token'];
        print('Token: $token');
        print('Response: ${response.statusCode}');
        print('Body: ${response.body}');
        await TokenService.saveToken(token);
        return true;

      }
      return false;
    } catch (e) {
      return false;
    }
  }

  static Future<UserProfile> getCurrentUser() async {
    final token = await TokenService.getToken();

    final response = await http.get(
      Uri.parse('$_baseUrl/me'),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json'
      },
    );

    if (response.statusCode == 200) {
      return UserProfile.fromJson(json.decode(response.body));
    }
    throw Exception('Failed to load user profile');
  }

  static Future<void> logout() async {
    await TokenService.deleteToken();
  }
}