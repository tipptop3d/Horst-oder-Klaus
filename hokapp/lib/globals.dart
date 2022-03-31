import 'dart:io';
import 'dart:typed_data';

import 'package:flutter/material.dart';

const brickPort = 64010;
Stream<Uint8List>? broadcast;
bool isLifted = false;

class ThemeModeNotifier extends ValueNotifier<ThemeMode> {
  ThemeModeNotifier(ThemeMode value) : super(value);

  bool isLight() => value == ThemeMode.light;
  bool isDark() => value == ThemeMode.dark;
  bool isSystem() => value == ThemeMode.system;

  void switchMode() {
    switch (value) {
      case ThemeMode.light:
        value = ThemeMode.dark;
        break;
      case ThemeMode.dark:
        value = ThemeMode.light;
        break;
      case ThemeMode.system:
        break;
    }
  }
}

final themeMode = ThemeModeNotifier(ThemeMode.dark);

class SendInfoNotifier extends ValueNotifier<bool> {
  String? _tex;
  Socket? _socket;
  SendInfoNotifier(bool value) : super(value);

  String? get tex {
    return _tex;
  }

  set tex(String? tex) {
    _tex = tex;
    checkCanSend();
  }

  Socket? get socket {
    return _socket;
  }

  set socket(Socket? socket) {
    _socket = socket;
    if (checkCanSend()) {
      broadcast = _socket?.asBroadcastStream();
    }
  }

  bool checkCanSend() {
    value = _socket != null && _tex != null;
    return value;
  }
}

final sendInfo = SendInfoNotifier(false);
