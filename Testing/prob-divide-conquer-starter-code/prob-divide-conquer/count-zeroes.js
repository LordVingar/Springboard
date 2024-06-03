function countZeroes(arr) {
    // Helper function to perform binary search for the first occurrence of 0
    function findFirstZero(arr) {
      let low = 0;
      let high = arr.length - 1;
      
      while (low <= high) {
        let mid = Math.floor((low + high) / 2);
        
        // Check if mid is the first occurrence of 0
        if (arr[mid] === 0 && (mid === 0 || arr[mid - 1] === 1)) {
          return mid;
        } else if (arr[mid] === 1) {
          low = mid + 1;
        } else {
          high = mid - 1;
        }
      }
      return -1;  // In case there are no zeroes in the array
    }
  
    // Find the first occurrence of 0 in the array
    const firstZeroIndex = findFirstZero(arr);
    
    // If there are no zeroes in the array, return 0
    if (firstZeroIndex === -1) {
      return 0;
    }
    
    // The number of zeroes is the length of the array minus the index of the first 0
    return arr.length - firstZeroIndex;
  }
  
  module.exports = countZeroes;