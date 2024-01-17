payments.test.js
describe("Payments test (with setup and tear-down)", function() {
  beforeEach(function () {
    // initialization logic
    billAmtInput.value = '30';
    tipAmtInput.value = '5';
    paymentForm.reset();
  });

  it('should add a new payment to allPayments on submitPaymentInfo()', function () {
    submitPaymentInfo();

    expect(Object.keys(allPayments).length).toEqual(1);
    expect(allPayments['payment1'].billAmt).toEqual('30');
    expect(allPayments['payment1'].tipAmt).toEqual('5');
    expect(allPayments['payment1'].tipPercent).toEqual(17);
  });

  it('should update paymentTable with new payment on submitPaymentInfo()', function () {
    submitPaymentInfo();

    const paymentRows = paymentTbody.querySelectorAll('tr');

    expect(paymentRows.length).toEqual(1);
    expect(paymentRows[0].querySelectorAll('td')[0].innerText).toEqual('$30');
    expect(paymentRows[0].querySelectorAll('td')[1].innerText).toEqual('$5');
    expect(paymentRows[0].querySelectorAll('td')[2].innerText).toEqual('17%');
  });

  afterEach(function() {
    // teardown logic
    paymentTbody.innerHTML = '';
    allPayments = {};
    paymentId = 0;
  });
});