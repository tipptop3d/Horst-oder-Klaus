import 'dart:io';

import 'package:flutter/material.dart';

import 'package:network_info_plus/network_info_plus.dart';
import 'package:network_tools/network_tools.dart';

import '../globals.dart';
import 'hok_appbar.dart';

class SetConnectionMenu extends StatelessWidget {
  const SetConnectionMenu({Key? key}) : super(key: key);

  static const routeName = '/search';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: const HokAppBar(),
      body: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Container(
              width: 180,
              padding: const EdgeInsets.all(8.0),
              child: const CustomIPField(),
            ),
          ),
          const Expanded(
            child: SearchResults(),
          ),
        ],
      ),
    );
  }
}

class CustomIPField extends StatelessWidget {
  const CustomIPField({
    Key? key,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return TextField(
      onSubmitted: (value) async {
        try {
          sendInfo.socket = await Socket.connect(
            value,
            brickPort,
          );
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('Connected to $value'),
            ),
          );
          Navigator.popAndPushNamed(context, '/input');
        } on Exception catch (e) {
          showErrorDialog(context, e);
        }
      },
      keyboardType: const TextInputType.numberWithOptions(
        decimal: true,
      ),
    );
  }
}

class SearchResults extends StatefulWidget {
  const SearchResults({Key? key}) : super(key: key);

  @override
  State<SearchResults> createState() => _SearchResultsState();
}

class _SearchResultsState extends State<SearchResults> {
  final Future<String?> _ip = NetworkInfo().getWifiIP();
  late Stream<OpenPort> deviceStream;
  List<OpenPort> devices = <OpenPort>[];

  @override
  Widget build(BuildContext context) {
    devices.clear();
    return Center(
      child: FutureBuilder<Stream<OpenPort>>(
        future: _discoverPort(),
        builder: (context, snapshot) {
          if (snapshot.hasError) {
            return Text(
              'Error: ${snapshot.error.toString()}',
              style: const TextStyle(color: Colors.red),
            );
          } else if (!snapshot.hasData) {
            return const CircularProgressIndicator(
              color: Colors.black26,
            );
          } else {
            return StreamBuilder<OpenPort>(
              stream: deviceStream,
              builder: (context, snapshot) {
                if (!snapshot.hasData) {
                  return const CircularProgressIndicator(
                    color: Colors.black26,
                  );
                } else {
                  OpenPort device = snapshot.data!;
                  if (!devices.contains(device)) {
                    devices.add(device);
                  }
                  return RefreshIndicator(
                    onRefresh: _pullRefresh,
                    child: ListView.builder(
                      padding: const EdgeInsets.all(8),
                      itemCount: devices.length,
                      itemBuilder: (context, index) {
                        return ConnectionTile(devices[index]);
                      },
                    ),
                  );
                }
              },
            );
          }
        },
      ),
    );
  }

  Future<Stream<OpenPort>> _discoverPort() async {
    devices.clear();
    String? ip = await _ip;
    if (ip == null) {
      throw Exception('No IP found. Maybe on mobile data?');
    }
    final String subnet = ip.substring(0, ip.lastIndexOf('.'));
    setState(() {
      deviceStream = HostScanner.discoverPort(
        subnet,
        brickPort,
        resultsInIpAscendingOrder: false,
        timeout: const Duration(seconds: 3),
      );
    });
    return deviceStream;
  }

  Future<void> _pullRefresh() async {
    await _discoverPort();
    await Future.delayed(const Duration(seconds: 2));
  }
}

class ConnectionTile extends StatefulWidget {
  final OpenPort addr;
  const ConnectionTile(this.addr, {Key? key}) : super(key: key);

  @override
  State<ConnectionTile> createState() => _ConnectionTileState();
}

class _ConnectionTileState extends State<ConnectionTile> {
  bool _isLoading = false;
  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 2),
      child: ListTile(
        contentPadding: const EdgeInsets.only(left: 16),
        tileColor: Colors.black12,
        enabled: widget.addr.isOpen,
        title: Text(widget.addr.ip),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
        ),
        trailing: ElevatedButton(
          style: ElevatedButton.styleFrom(
            //primary: Colors.black12,
            shape: const RoundedRectangleBorder(
              borderRadius: BorderRadius.horizontal(
                right: Radius.circular(12),
              ),
            ),
            elevation: 0,
            minimumSize: const Size(90, double.infinity),
          ),
          onPressed: (!_isLoading && widget.addr.isOpen)
              ? () async {
                  setState(() {
                    _isLoading = true;
                  });
                  try {
                    sendInfo.socket = await Socket.connect(
                      widget.addr.ip,
                      widget.addr.port,
                      timeout: const Duration(seconds: 3),
                    );
                    ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                        content: Text('Connected to ${widget.addr.ip}')));
                    Navigator.popAndPushNamed(context, '/home');
                  } on Exception catch (e) {
                    showErrorDialog(context, e);
                  }
                  setState(() {
                    _isLoading = false;
                  });
                }
              : null,
          child: _isLoading
              ? const CircularProgressIndicator()
              : const Text('Connect'),
        ),
      ),
    );
  }
}

void showErrorDialog(BuildContext context, Exception e) {
  showDialog(
    context: context,
    builder: (context) => AlertDialog(
      title: const Text('Error while connecting'),
      content: Text(e.toString()),
      actions: [
        TextButton(
          onPressed: () {
            Navigator.pop(context);
          },
          child: const Text('OK'),
        )
      ],
    ),
  );
}
