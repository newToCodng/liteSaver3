import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import '../models/category_model.dart';
import '../service/token_service.dart';

class CategoryService {
  static const String _baseUrl = 'http://your-backend/api/transactions';

  static Future<List<CategoryModel>> getCategories() async {
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
      return data.map((json) => CategoryModel.fromJson(json)).toList();
    }
    throw Exception('Failed to load categories');
  }

  static Future<int> createCategory(CategoryModel category) async {
    final token = await TokenService.getToken();
    final response = await http.post(
      Uri.parse(_baseUrl),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json'
      },
      body: json.encode({
        'category_id': category.categoryId,
        'name': category.name,
        'category_type': category.category_type,
      }),
    );

    if (response.statusCode == 200) {
      return json.decode(response.body)['category_id'];
    }
    throw Exception('Failed to create category');
  }
}