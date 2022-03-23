import 'package:flutter/material.dart';
import 'globals.dart';

import 'theme.dart';
import 'widgets/draw.dart';
import 'widgets/home.dart';
import 'widgets/set_connection.dart';

Future<void> main() async {
  runApp(const HokApp());
}

class HokApp extends StatelessWidget {
  const HokApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return ValueListenableBuilder<ThemeMode>(
      valueListenable: themeMode,
      builder: (context, value, widget) => MaterialApp(
        title: 'Horst oder Klaus',
        theme: hokThemeLight,
        darkTheme: hokThemeDark,
        themeMode: value,
        initialRoute: '/home',
        routes: {
          HomeMenu.routeName: (context) => const HomeMenu(),
          SetConnectionMenu.routeName: (context) => const SetConnectionMenu(),
          ExpressionDraw.routeName: (context) => const ExpressionDraw(),
        },
      ),
    );
  }
}
