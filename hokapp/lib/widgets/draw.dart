import 'dart:convert';
import 'dart:io';
import 'dart:typed_data';

import 'package:flutter/material.dart';
import 'package:flutter_math_fork/flutter_math.dart';
import 'package:math_expressions/math_expressions.dart';
import 'package:math_keyboard/math_keyboard.dart';
import '../globals.dart';

final lexer = Lexer();

class ExpressionDraw extends StatelessWidget {
  const ExpressionDraw({Key? key}) : super(key: key);

  static const routeName = '/draw';

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      body: DrawProgression(),
    );
  }
}

class DrawProgression extends StatefulWidget {
  const DrawProgression({Key? key}) : super(key: key);

  @override
  State<DrawProgression> createState() => _DrawProgressionState();
}

class _DrawProgressionState extends State<DrawProgression> {
  late List<int> expressionBytes;
  late final Socket socket;

  @override
  void initState() {
    assert(sendInfo.tex != null);
    Expression expr = TeXParser(sendInfo.tex!).parse();
    expressionBytes = ascii.encode(lexer
        .tokenizeToRPN(expr.toString())
        .map((e) => e.toString().replaceAll(' ', ''))
        .join('\x1f'));
    sendInfo.socket!.add(expressionBytes);
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const Text(
            'Drawing',
            textScaleFactor: 2,
          ),
          Padding(
            padding: const EdgeInsets.symmetric(vertical: 8.0),
            child: StreamBuilder<Uint8List>(
              stream: broadcast,
              initialData: Uint8List.fromList([0]),
              builder: (context, snapshot) {
                ByteData bytes = snapshot.data!.buffer.asByteData();
                return LinearProgressIndicator(
                  value: bytes.getUint8(0) / 255.0,
                  color: Theme.of(context).primaryColorLight,
                );
              },
            ),
          ),
          Math.tex(
            '\\boxed{${sendInfo.tex}}',
            textScaleFactor: 1.5,
          ),
        ],
      ),
    );
  }
}
