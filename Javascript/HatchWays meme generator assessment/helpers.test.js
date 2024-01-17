helpers.test.js
describe("Helpers test", function() {
  it('should correctly sum payment total for billAmt', function () {
    const payment1 = { billAmt: 10, tipAmt: 2, tipPercent: 20 };
    const payment2 = { billAmt: 20, tipAmt: 4, tipPercent: 20 };

    allPayments = { payment1, payment2 };

    const result = sumPaymentTotal('billAmt');

    expect(result).toEqual(30);
  });

  it('should correctly calculate tip percent', function () {
    const result = calculateTipPercent(20, 5);

    expect(result).toEqual(25);
  });
});