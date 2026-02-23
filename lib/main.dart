import 'package:flutter/material.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(title: Text("AI Auto Fix Test")),
        body: Center(
          child: Text("Galti pakdo!") // Semicolon missing yahan
        ),
      ),
    );
  // Closing brace missing yahan
