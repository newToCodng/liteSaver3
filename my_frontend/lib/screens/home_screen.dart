import 'package:flutter/material.dart';
//import 'dart:convert';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
      return Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
              colors: [
                Color(0xFF0D47A1),   // Dark Blue
                Color(0xFF6A1B9A),    // Purple
              ],
          ),
        ),
        child: Scaffold(
          backgroundColor: Colors.transparent,
          appBar: AppBar(
              title: const Text('Spy Save'),
              backgroundColor: Colors.transparent,
              elevation: 0,
          ),
          body: Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text(
                      'Welcome to Spy Save, start saving now!',
                      style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                        color: Colors.white
                      ),
                  ),
                  SizedBox(height: 150),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      ElevatedButton(
                          onPressed: () {
                            Navigator.pushNamed(context, '/login');
                          },
                          child: Text(
                            'Login',
                             style: Theme.of(context).textTheme.bodyMedium
                          ),
                      ),
                      SizedBox(width: 10),
                      ElevatedButton(onPressed:() {
                        Navigator.pushNamed(context, '/register');
                        },
                        child: Text('Register', style: Theme.of(context).textTheme.bodyMedium),
                      )
                    ],
                  )
                ]
              )
          ),
        )
        );
      }
    }
