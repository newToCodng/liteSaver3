import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'screens/home_screen2.dart';
import 'screens/register_screen.dart';
import 'screens/login_screen.dart';
import 'screens/forgotten_password_screen.dart';
import 'screens/dash_board_screen.dart';
import 'screens/add_transaction_screen.dart';


void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    final Map<String, WidgetBuilder> routes = {
      '/': (context) => HomeScreen(),
      '/register': (context) => RegisterScreen(),
      '/login' : (context) => LoginScreen(),
      '/forgotPassword': (context) => ForgotPasswordScreen(),
      '/dashboard': (context) => MainDashboard(),
      '/add-transaction': (context) => AddTransactionScreen(),
    };

    return MaterialApp(
      title: 'LiteSaver',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurpleAccent),
        scaffoldBackgroundColor: Colors.white,
        useMaterial3: true,
        textTheme: TextTheme(
          bodyLarge: TextStyle(fontFamily: "Segoe UI"),
          bodyMedium: TextStyle(fontFamily: "segoe UI")
        ),
        appBarTheme: AppBarTheme(
          backgroundColor: Colors.blue,
          titleTextStyle: TextStyle(
            fontFamily: "Segoe UI",
            fontSize: 20,
            fontWeight: FontWeight.bold,
            color: Colors.white
          ),
        ),
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            backgroundColor: Colors.blue,
            textStyle: TextStyle(fontFamily: "Segoe UI"),
          ),
        ),
      ),
      routes: routes
      );
  }
}