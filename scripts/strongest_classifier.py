#! /usr/bin/env python3

import csv, sys
from functools import reduce

def read_phone(filename):
  with open(filename, 'r') as infile:
    reader = csv.DictReader(infile)
    data = {}
    for row in reader:
      for header, value in row.items():
        try:
          data[header].append(value)
        except KeyError:
          data[header] = [value]
  return data

def read_phones(filename):
  with open(filename, "r") as f:
    reader = csv.DictReader(f)
    return list(reader)

def intersect(phone_1, phone_2):
  return dict(phone_1.items() & phone_2.items())

def print_phone(phone):
  for (feature, value) in phone.items():
    if value == "+":
      print(feature)
    elif value == "-":
      print("not " + feature)
    elif value == "#":
      print("#" + feature)

def remove_indices(index_list,target_list):
  for index in sorted(index_list, reverse=True):
    del target_list[index]
  return target_list

def add_indices(index_list,target_list):
  ntarget = []
  for index in sorted(index_list):
    ntarget.append(target_list[index])
  return ntarget

def check_neg(filename,dictionary):
  data = read_phone(filename)
  ndict = dictionary.copy()
  target_indices = ([i for i, x in enumerate(data["target"]) if x == "1"])
  for key,value in dictionary.items():
    if any(value == x for x in remove_indices(target_indices, data[key])):
      del ndict[key]
    return ndict

def context(filename):
  phones = read_phones(filename)
  selected_phones = filter(lambda phone: phone["target"] == "1", phones)
  classifier = reduce(intersect, selected_phones)
  new_classifier = check_neg(filename,classifier)
  return new_classifier

def classifier(filename):
  filename = sys.argv[1]
  phones = read_phones(filename)
  selected_phones = filter(lambda phone: phone["target"] == "1", phones)
  classifier = reduce(intersect, selected_phones)
  new_classifier = {k:v for (k, v) in classifier.items() if not k.startswith('L') and not k.startswith('R') and k != "target"}
  return new_classifier