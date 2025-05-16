import 'package:flutter/material.dart';
import 'dart:math';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;

    return Scaffold(
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [
              Colors.blue.shade800,
              Colors.purple.shade600,
            ],
          ),
        ),
        child: Stack(
          children: [
            // Background floating elements
            Positioned(
              top: size.height * 0.15,
              left: size.width * 0.2,
              child: _FloatingCircle(size: size.width * 0.4),
            ),
            Positioned(
              top: size.height * 0.8,
              right: size.width * 0.1,
              child: _FloatingCircle(size: size.width * 0.4),
            ),

            Positioned(
              top: size.height * 0.8,
              right: size.width * 0.3,
              child: _FloatingCircle(size: size.width * 0.4),
            ),
            // Content
            SafeArea(
              child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 24.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const SizedBox(height: 40),

                    // Hero Section
                    _buildHeroSection(context),

                    const SizedBox(height: 40),

                    // Feature Cards
                    _buildFeatureGrid(),

                    const SizedBox(height: 40),

                    // Auth Buttons
                    _buildAuthButtons(context),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildHeroSection(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Your Smart Savings\nCompanion',
          style: Theme.of(context).textTheme.headlineMedium?.copyWith(
            color: Colors.white,
            fontWeight: FontWeight.bold,
            height: 1.2,
          ),
        ),
        const SizedBox(height: 16),
        Text(
          'Track, save, and grow your money smarter with AI-powered insights',
          style: Theme.of(context).textTheme.bodyLarge?.copyWith(
            color: Colors.white70,
          ),
        ),
      ],
    );
  }

  Widget _buildFeatureGrid() {
    return GridView.count(
      shrinkWrap: true,
      crossAxisCount: 2,
      childAspectRatio: 1.2,
      crossAxisSpacing: 16,
      mainAxisSpacing: 16,
      children: [
        _FeatureCard(
          icon: Icons.auto_graph_rounded,
          title: 'AI Insights',
          color: Colors.blue.shade200,
        ),
        _FeatureCard(
          icon: Icons.account_balance_wallet_rounded,
          title: 'Smart Budgets',
          color: Colors.purple.shade200,
        ),
        _FeatureCard(
          icon: Icons.security_rounded,
          title: 'Safe & Secure',
          color: Colors.green.shade200,
        ),
        _FeatureCard(
          icon: Icons.notifications_active_rounded,
          title: 'Reminders',
          color: Colors.orange.shade200,
        ),
      ],
    );
  }

  Widget _buildAuthButtons(BuildContext context) {
    return Column(
      children: [
        _AuthButton(
          text: 'Get Started',
          icon: Icons.rocket_launch_rounded,
          onPressed: () => Navigator.pushNamed(context, '/register'),
          color: Colors.white,
          textColor: Colors.blue.shade800,
        ),
        const SizedBox(height: 16),
        _AuthButton(
          text: 'I Have an Account',
          icon: Icons.login_rounded,
          onPressed: () => Navigator.pushNamed(context, '/login'),
          color: Colors.white24,
          textColor: Colors.white,
        ),
      ],
    );
  }
}

// Custom Widgets
class _FloatingCircle extends StatelessWidget {
  final double size;

  const _FloatingCircle({required this.size});

  @override
  Widget build(BuildContext context) {
    return Transform.rotate(
      angle: pi / 4,
      child: Container(
        width: size,
        height: size,
        decoration: BoxDecoration(
          shape: BoxShape.circle,
          color: Colors.white.withValues(alpha: 0.09),
        ),
      ),
    );
  }
}

class _FeatureCard extends StatelessWidget {
  final IconData icon;
  final String title;
  final Color color;

  const _FeatureCard({
    required this.icon,
    required this.title,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 4,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(20),
      ),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, size: 32, color: color),
            const SizedBox(height: 8),
            Text(title,
              style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                fontWeight: FontWeight.w500,
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _AuthButton extends StatelessWidget {
  final String text;
  final IconData icon;
  final VoidCallback onPressed;
  final Color color;
  final Color textColor;

  const _AuthButton({
    required this.text,
    required this.icon,
    required this.onPressed,
    required this.color,
    required this.textColor,
  });

  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      onPressed: onPressed,
      style: ElevatedButton.styleFrom(
        backgroundColor: color,
        padding: const EdgeInsets.symmetric(vertical: 18, horizontal: 24),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(15),
        ),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(icon, color: textColor),
          const SizedBox(width: 12),
          Text(text,
            style: Theme.of(context).textTheme.bodyLarge?.copyWith(
              color: textColor,
              fontWeight: FontWeight.w600,
            ),
          ),
        ],
      ),
    );
  }
}