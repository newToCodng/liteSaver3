import 'package:flutter/material.dart';
import '../models/user_model.dart';
import '../service/auth_service.dart';
import '../service/user_service.dart';
import 'add_transaction_screen.dart';


class MainDashboard extends StatefulWidget {
  @override
  _MainDashboardState createState() => _MainDashboardState();
}


class _MainDashboardState extends State<MainDashboard> {
  int _currentIndex = 0;
  final PageController _pageController = PageController(viewportFraction: 0.8);
  late Future<UserProfile> _userProfile;

  @override
  void initState() {
    super.initState();
    _userProfile = AuthService.getCurrentUser();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Financial Dashboard'),
        actions: [
          FutureBuilder<UserProfile>(
            future: _userProfile,
            builder: (context, snapshot) {
              if (snapshot.connectionState == ConnectionState.waiting) {
                return Padding(
                  padding: EdgeInsets.only(right: 20.0),
                  child: Center(child: CircularProgressIndicator()),
                );
              }
              if (snapshot.hasError) {
                return Padding(
                    padding: EdgeInsets.only(right: 20.0),
                    child: Tooltip(
                      message: 'Error loading profile',
                      child: Icon(Icons.error, color: Colors.red),
                    ));
                    }
                    return Padding(
                    padding: EdgeInsets.only(right: 20.0),
              child: Center(
              child: Text(
              'Hi ${snapshot.data!.firstName}',
              style: TextStyle(
              fontSize: 14,
              color: Colors.white70,
              ),
              ),
              ),
              );
            },
          ),
        ],
      ),
      body: SingleChildScrollView(
        child: Column(
          children: [
            SizedBox(height: 20),
            _buildSlidingCards(),
            SizedBox(height: 30),
            _buildActionButtons(),
          ],
        ),
      ),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _currentIndex,
        onTap: (index) => _handleNavigation(index, context),
        items: [
          BottomNavigationBarItem(
            icon: Icon(Icons.home),
            label: 'Home',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.add),
            label: 'Transactions',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.person),
            label: 'Profile',
          ),
        ],
      ),
    );
  }

  void _handleNavigation(int index, BuildContext context) {
    setState(() => _currentIndex = index);
    if (index == 1) {
      Navigator.push(context, MaterialPageRoute(
          builder: (context) => AddTransactionScreen(
            onTransactionAdded: () {
              setState(() {
                _userProfile = UserService().getCurrentUserProfile();
              });
            },
      )));
    }
    if (index == 2) {
      Navigator.push(context, MaterialPageRoute(builder: (context) => ProfileScreen()));
    }
  }

  Widget _buildSlidingCards() {
    return SizedBox(
      height: 200,
      child: PageView(
        controller: _pageController,
        scrollDirection: Axis.horizontal,
        children: [
          _buildCard('GBP', '\$5,432.00', Colors.blue),
          _buildCard('USD', '\$2,500.00', Colors.green),
          _buildCard('NGN', '\$1,200.00', Colors.orange),
        ],
      ),
    );
  }

  Widget _buildCard(String title, String amount, Color color) {
    return Container(
      margin: EdgeInsets.symmetric(horizontal: 10),
      decoration: BoxDecoration(
        color: color,
        borderRadius: BorderRadius.circular(15),
        boxShadow: [
          BoxShadow(
            color: Colors.black12,
            blurRadius: 10,
            offset: Offset(0, 5),
          ),
        ],
      ),
      child: Padding(
        padding: EdgeInsets.all(20),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              title,
              style: TextStyle(
                color: Colors.white70,
                fontSize: 18,
              ),
            ),
            SizedBox(height: 10),
            Text(
              amount,
              style: TextStyle(
                color: Colors.white,
                fontSize: 32,
                fontWeight: FontWeight.bold,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildActionButtons() {
    return Padding(
      padding: EdgeInsets.symmetric(horizontal: 20),
      child: Column(
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              _buildActionButton(Icons.pie_chart, 'Budget Report'),
              _buildActionButton(Icons.history, 'Transaction History'),
              _buildActionButton(Icons.settings, 'Settings'),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildActionButton(IconData icon, String label) {
    return Column(
      children: [
        IconButton(
          icon: Icon(icon, size: 30),
          color: Colors.blue,
          onPressed: () {},
        ),
        Text(
          label,
          style: TextStyle(fontSize: 12),
        ),
      ],
    );
  }
}


// Placeholder screens for navigation
class ProfileScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) => Scaffold(appBar: AppBar(title: Text('Profile')));
}