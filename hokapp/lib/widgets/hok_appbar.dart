import 'package:flutter/material.dart';

import 'package:flutter_svg/svg.dart';

import '../globals.dart';

class HokAppBar extends StatelessWidget implements PreferredSizeWidget {
  const HokAppBar({Key? key}) : super(key: key);
  @override
  Size get preferredSize => const Size.fromHeight(70.0);

  @override
  Widget build(BuildContext context) {
    ThemeData theme = Theme.of(context);
    Color color = theme.primaryTextTheme.bodyLarge?.color ?? theme.cardColor;

    return SafeArea(
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 5.0),
        decoration: BoxDecoration(
          color: theme.primaryColor,
          border: Border(
            bottom: BorderSide(
              color: color,
              width: 2.0,
            ),
          ),
        ),
        child: Stack(
          children: [
            Center(
              child: SvgPicture.asset(
                'assets/logo_light.svg',
                height: 60.0,
                color: color,
                semanticsLabel: 'HoK Logo',
              ),
            ),
            const Align(
              alignment: Alignment.centerRight,
              child: LightSwitch(),
            ),
          ],
        ),
      ),
    );
  }
}

class LightSwitch extends StatefulWidget {
  const LightSwitch({Key? key}) : super(key: key);

  @override
  State<LightSwitch> createState() => _LightSwitchState();
}

class _LightSwitchState extends State<LightSwitch>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _animation;

  @override
  void initState() {
    _controller = AnimationController(
      duration: const Duration(seconds: 1),
      vsync: this,
    );
    _animation = Tween<double>(begin: 0.0, end: 1.0).animate(_controller);
    super.initState();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    _controller.forward();
    return IconButton(
      color: Colors.white,
      iconSize: 28,
      icon: Container(
        decoration: BoxDecoration(
          borderRadius: const BorderRadius.all(Radius.circular(8)),
          border: Border.all(
            width: 2,
            color: Colors.white,
          ),
        ),
        child: FadeTransition(
          opacity: _animation,
          child: themeMode.isDark()
              ? const Icon(Icons.dark_mode)
              : themeMode.isLight()
                  ? const Icon(Icons.light_mode)
                  : const Icon(Icons.lock),
        ),
      ),
      onPressed: () {
        _controller.reverse();
        setState(() {
          themeMode.switchMode();
        });
      },
    );
  }
}
