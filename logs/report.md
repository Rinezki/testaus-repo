# Software testing Report 2.2
This is report of assignment 2.2 Practucal Unit Testing Frameworks, Mocking, Stubbing and Fakes.

---

### Coverage

---
---

### Mocking
#### Screenshots:![mocking screenshot](mocktestresults.png)

#### Summary:
Mock test checks that order placement handles correctly orders, unavailable items, and payment failures using mocked objects.

#### Reflections:
Making the tests helped me to better understand how to isolate components by using mocks. Mocking is a neat way to test logic without relying on real implementations.

---
---

### Stubbing
#### Screenshots:

#### Summary:

#### Reflections:

---
---

### Fakes
#### Screenshots:
![item price fake unittest](./item_price/item_price_fake_unittest.png)

#### Summary:
Fake testing for "item_price" is written in different file "item_price_fake". It's functions is same as item_price, but it makes its own file for testing.

#### Reflections:
Fakes is good in unit and integration testing, when tester doesn't want to use real inputs/outputs from the code.

---