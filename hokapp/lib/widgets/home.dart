import 'package:flutter/material.dart';

import 'package:math_expressions/math_expressions.dart';
import 'package:math_keyboard/math_keyboard.dart';

import '../globals.dart';
import 'hok_appbar.dart';

final Lexer l = Lexer();

class HomeMenu extends StatelessWidget {
  const HomeMenu({Key? key}) : super(key: key);

  static const routeName = '/home';

  @override
  Widget build(BuildContext context) {
    return MathKeyboardViewInsets(
      child: Scaffold(
        appBar: const HokAppBar(),
        body: Center(
          child: Padding(
            padding:
                const EdgeInsets.symmetric(horizontal: 60.0, vertical: 20.0),
            child: Column(
              children: [
                const Padding(
                  padding: EdgeInsets.only(bottom: 16.0),
                  child: ConnectionMenu(),
                ),
                MathField(
                  decoration: InputDecoration(
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(60.0),
                    ),
                    labelText: 'Expression',
                  ),
                  onChanged: (String value) {
                    try {
                      TeXParser(value).parse();
                      sendInfo.tex = value;
                    } catch (e) {
                      sendInfo.tex = null;
                    }
                  },
                ),
                const LiftedCheckBox()
              ],
            ),
          ),
        ),
        floatingActionButtonLocation: FloatingActionButtonLocation.centerFloat,
        floatingActionButton: const DrawActionButton(),
      ),
    );
  }
}

class LiftedCheckBox extends StatefulWidget {
  const LiftedCheckBox({Key? key}) : super(key: key);

  @override
  State<LiftedCheckBox> createState() => _LiftedCheckBoxState();
}

class _LiftedCheckBoxState extends State<LiftedCheckBox> {
  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        const Text('Pen Lifted?'),
        Checkbox(
            value: isLifted,
            onChanged: (bool? value) {
              setState(() {
                isLifted = value!;
              });
            })
      ],
    );
  }
}

class ConnectionMenu extends StatefulWidget {
  const ConnectionMenu({Key? key}) : super(key: key);

  @override
  State<ConnectionMenu> createState() => _ConnectionMenuState();
}

class _ConnectionMenuState extends State<ConnectionMenu> {
  @override
  Widget build(BuildContext context) {
    return ValueListenableBuilder<bool>(
      valueListenable: sendInfo,
      builder: (context, value, widget) {
        if (sendInfo.socket == null) {
          return ElevatedButton.icon(
            onPressed: () {
              Navigator.pushNamed(context, '/search');
            },
            icon: const Icon(Icons.settings_remote_outlined),
            label: const Text('Connect to Brick'),
          );
        } else {
          return ElevatedButton(
            onPressed: () async {
              sendInfo.socket!.destroy();
              sendInfo.socket = null;
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(
                  content: Text('Disconnected'),
                ),
              );
            },
            child: const Text('Disconnect'),
          );
        }
      },
    );
  }
}

enum InvalidCause { expression, ip, unknown }

class DrawActionButton extends StatefulWidget {
  const DrawActionButton({Key? key}) : super(key: key);

  @override
  State<DrawActionButton> createState() => _DrawActionButtonState();
}

class _DrawActionButtonState extends State<DrawActionButton>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation _animation;
  bool isLoading = false;

  @override
  void initState() {
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 200),
    );
    super.initState();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    ThemeData theme = Theme.of(context);
    _animation = ColorTween(
      begin: theme.disabledColor,
      end: theme.buttonTheme.colorScheme!.primary,
    ).animate(_controller);

    return SizedBox(
      height: 50,
      width: 110,
      child: ValueListenableBuilder<bool>(
        valueListenable: sendInfo,
        builder: (context, active, widget) {
          return AnimatedBuilder(
            animation: _animation,
            builder: (context, child) {
              active ? _controller.forward() : _controller.reverse();
              return FloatingActionButton.extended(
                onPressed: active
                    ? () {
                        Navigator.pushNamed(context, '/draw');
                      }
                    : () {
                        InvalidCause cause = InvalidCause.unknown;
                        String message = 'Unknown error';
                        if (sendInfo.socket == null) {
                          cause = InvalidCause.ip;
                          message = 'No Connection';
                        } else if (sendInfo.tex == null) {
                          cause = InvalidCause.expression;
                          message = 'Invalid Expression given';
                        }
                        showSnackBarInvalid(context, cause, message);
                      },
                label: const Text(
                  'Draw',
                ),
                backgroundColor: _animation.value,
              );
            },
          );
        },
      ),
    );
  }
}

bool sBInvalidShowing = false;

void showSnackBarInvalid(
    BuildContext context, InvalidCause cause, String message) {
  if (sBInvalidShowing) {
    return;
  }

  sBInvalidShowing = true;

  ScaffoldMessenger.of(context)
      .showSnackBar(
        SnackBar(
          content: Text(
            message,
          ),
          duration: const Duration(seconds: 2),
          action: cause == InvalidCause.ip
              ? SnackBarAction(
                  label: 'Connect',
                  onPressed: () => Navigator.pushNamed(context, '/search'),
                )
              : null,
        ),
      )
      .closed
      .then(
    (SnackBarClosedReason reason) {
      sBInvalidShowing = false;
    },
  );
}
