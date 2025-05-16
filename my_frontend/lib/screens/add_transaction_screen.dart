import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:my_frontend/models/transaction_model.dart';
import 'package:my_frontend/models/account_model.dart';
import 'package:my_frontend/models/category_model.dart';
import 'package:my_frontend/service/account_service.dart';
import 'package:my_frontend/service/transaction_service.dart';
import 'package:my_frontend/service/category_service.dart';


class AddTransactionScreen extends StatefulWidget {
  final VoidCallback? onTransactionAdded;

  AddTransactionScreen({this.onTransactionAdded});

  @override
  _AddTransactionScreenState createState() => _AddTransactionScreenState();
}

class _AddTransactionScreenState extends State<AddTransactionScreen> {
  final _formKey = GlobalKey<FormState>();
  List<Account> _accounts = [];
  List<CategoryModel> _categories = [];
  int? _selectedAccountId;
  int? _selectedCategoryId;
  final _amountController = TextEditingController();
  final _descriptionController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _loadInitialData();
  }

  Future<void> _loadInitialData() async {
    try {
      _accounts = await AccountService.getAccounts();
      _categories = await CategoryService.getCategories();
      setState(() {});
    } catch (e) {
      print('Error loading data: $e');
    }
  }


  Future<void> _submitTransaction() async {
    if (_formKey.currentState!.validate()) {
      final transaction = Transaction(
        accountId: _selectedAccountId!,
        categoryId: _selectedCategoryId!,
        amount: double.parse(_amountController.text),
        description: _descriptionController.text,
      );

      try {
        await TransactionService.createTransaction(transaction);
        widget.onTransactionAdded!();
        Navigator.pop(context);
      } catch (e) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Failed to create transaction: $e')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    // Check if accounts and categories are loaded
    if (_accounts.isEmpty || _categories.isEmpty) {
      return Scaffold(
        appBar: AppBar(title: Text('Add Transaction')),
        body: Center(child: CircularProgressIndicator()), // Show loading indicator
      );
    }

    return Scaffold(
      appBar: AppBar(title: Text('Add Transaction')),
      body: Form(
        key: _formKey,
        child: ListView(
          padding: EdgeInsets.all(16),
          children: [
            DropdownButtonFormField<int>(
              items: _accounts.map((account) => DropdownMenuItem(
                value: account.accountId,
                child: Text(account.name),
              )).toList(),
              onChanged: (value) => setState(() {
                _selectedAccountId = value;
              }),
              decoration: InputDecoration(labelText: 'Account'),
            ),
            DropdownButtonFormField<int>(
              items: _categories.map((category) => DropdownMenuItem(
                value: category.categoryId,
                child: Text(category.name),
              )).toList(),
              onChanged: (value) => setState(() {
                _selectedCategoryId = value;
              }),
              decoration: InputDecoration(labelText: 'Category'),
            ),
            TextFormField(
              controller: _amountController,
              keyboardType: TextInputType.number,
              validator: (value) => value?.isEmpty ?? true ? 'Required' : null,
              decoration: InputDecoration(labelText: 'Amount'),
            ),
            TextFormField(
              controller: _descriptionController,
              validator: (value) => value?.isEmpty ?? true ? 'Required' : null,
              decoration: InputDecoration(labelText: 'Description'),
            ),
            ElevatedButton(
              onPressed: _submitTransaction,
              child: Text('Add Transaction'),
            ),
          ],
        ),
      ),
    );
  }
}