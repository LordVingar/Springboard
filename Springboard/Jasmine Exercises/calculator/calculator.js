window.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById("calc-form");
  if (form) {
    setupIntialValues();
    form.addEventListener("submit", function(e) {
      e.preventDefault();
      update();
    });
  }
});

function getCurrentUIValues() {
  return {
    amount: +(document.getElementById("loan-amount").value),
    years: +(document.getElementById("loan-years").value),
    rate: +(document.getElementById("loan-rate").value),
  }
}

// Get the inputs from the DOM.
// Put some default values in the inputs
// Call a function to calculate the current monthly payment
function setupIntialValues() {  // Set some default values in the inputs
  document.getElementById("loan-amount").value = 10000;
  document.getElementById("loan-years").value = 3;
  document.getElementById("loan-rate").value = 5;

  // Call a function to calculate the current monthly payment
  update();
}

// Get the current values from the UI
// Update the monthly payment
function update() {
  const values = getCurrentUIValues();
  updateMonthly(calculateMonthlyPayment(values));
}



// Given an object of values (a value has amount, years and rate ),
// calculate the monthly payment.  The output should be a string
// that always has 2 decimal places.
function calculateMonthlyPayment(values) {
  const monthlyRate = values.rate / 12 / 100;
  const totalPayments = values.years * 12;

  if (monthlyRate === 0) {
    return (values.amount / totalPayments).toFixed(2);
  }

  const monthlyPayment = (values.amount * monthlyRate) / (1 - Math.pow(1 + monthlyRate, -totalPayments));
  return monthlyPayment.toFixed(2);
}

// Given a string representing the monthly payment value,
// update the UI to show the value.
function updateMonthly(monthly) {
  const resultOutput = document.getElementById('monthly-payment');
  resultOutput.innerText = `$${monthly}`;
}
