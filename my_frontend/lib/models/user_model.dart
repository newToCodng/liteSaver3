class UserProfile {
  final int userId;
  final String firstName;
  final String lastName;
  final String email;

  UserProfile({
    required this.userId,
    required this.firstName,
    required this.lastName,
    required this.email,
  });

  factory UserProfile.fromJson(Map<String, dynamic> json) => UserProfile(
    userId: json['user_id'],
    firstName: json['first_name'],
    lastName: json['last_name'],
    email: json['email'],
  );
}