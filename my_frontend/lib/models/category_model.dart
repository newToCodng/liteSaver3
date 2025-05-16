class CategoryModel {
  final int categoryId;
  final String name;
  final List<Enum> category_type;

  CategoryModel({
    required this.categoryId,
    required this.name,
    required this.category_type,
  });

  factory CategoryModel.fromJson(Map<String, dynamic> json) => CategoryModel(
    categoryId: json['category_id'],
    name: json['name'].toDouble(),
    category_type: json['category_type'],
  );
}