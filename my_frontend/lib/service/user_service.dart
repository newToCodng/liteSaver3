import '../models/user_model.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';



class UserService {
  static const String _baseUrl = 'http://127.0.0.1:8000';
  final FlutterSecureStorage _storage = FlutterSecureStorage();

  Future<int> getCurrentUserId() async {
    final token = await _storage.read(key: 'auth_token');
    final response = await http.get(
      Uri.parse('$_baseUrl/me'),
      headers: {'Authorization': 'Bearer $token'},
    );

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return data['user_id'];
    }
    throw Exception('Failed to get current user ID');
  }

  Future<UserProfile> getCurrentUserProfile() async {
    final userId = await getCurrentUserId();
    final token = await _storage.read(key: 'auth_token');

    final response = await http.get(
      Uri.parse('$_baseUrl/users/$userId'),
      headers: {'Authorization': 'Bearer $token'},
    );

    if (response.statusCode == 200) {
      return UserProfile.fromJson(json.decode(response.body));
    }
    throw Exception('Failed to load user profile');
  }
}