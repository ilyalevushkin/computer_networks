import 'package:equatable/equatable.dart';
import 'package:flutter/material.dart';

class Turn extends Equatable {

  const Turn({
    required this.id
  });

  final int id;

  @override
  List<Object> get props => [id];
}