describe('Loan Calculator', function() {
  describe('calculateMonthlyPayment', function() {
    it('should calculate the monthly payment correctly', function() {
      // Arrange
      const values = {
        amount: 10000,
        years: 3,
        rate: 5,
      };

      // Act
      const result = calculateMonthlyPayment(values);

      // Assert
      expect(result).toEqual('299.71');
    });

    it('should handle zero interest rate correctly', function() {
      // Arrange
      const values = {
        amount: 10000,
        years: 3,
        rate: 0,
      };

      // Act
      const result = calculateMonthlyPayment(values);

      // Assert
      expect(result).toEqual('277.78');
    });

    it('should handle zero loan amount correctly', function() {
      // Arrange
      const values = {
        amount: 0,
        years: 3,
        rate: 5,
      };

      // Act
      const result = calculateMonthlyPayment(values);

      // Assert
      expect(result).toEqual('0.00');
    });

    // Add more test cases as needed

  });
});