import 'package:flutter/material.dart';

ThemeData hokThemeLight = ThemeData(
  brightness: Brightness.light,
  colorSchemeSeed: Colors.blue,
  fontFamily: 'Encode Sans Expanded',
  snackBarTheme: const SnackBarThemeData(
    contentTextStyle: TextStyle(color: Colors.black87),
    backgroundColor: Colors.white70,
    behavior: SnackBarBehavior.floating,
  ),
);

ThemeData hokThemeDark = ThemeData(
  brightness: Brightness.dark,
  colorSchemeSeed: Colors.lime,
  fontFamily: 'Encode Sans Expanded',
  snackBarTheme: const SnackBarThemeData(
    contentTextStyle: TextStyle(color: Colors.white70),
    backgroundColor: Colors.black54,
    behavior: SnackBarBehavior.floating,
  ),
);
