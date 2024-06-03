function sortedFrequency(arr, num) {
    // Helper function to find the first occurrence of num
    function findFirstOccurrence(arr, num) {
      let low = 0;
      let high = arr.length - 1;
      let result = -1;
      
      while (low <= high) {
        let mid = Math.floor((low + high) / 2);
        
        if (arr[mid] === num) {
          result = mid;
          high = mid - 1;  // Continue to search in the left half
        } else if (arr[mid] < num) {
          low = mid + 1;
        } else {
          high = mid - 1;
        }
      }
      
      return result;
    }
  
    // Helper function to find the last occurrence of num
    function findLastOccurrence(arr, num) {
      let low = 0;
      let high = arr.length - 1;
      let result = -1;
      
      while (low <= high) {
        let mid = Math.floor((low + high) / 2);
        
        if (arr[mid] === num) {
          result = mid;
          low = mid + 1;  // Continue to search in the right half
        } else if (arr[mid] < num) {
          low = mid + 1;
        } else {
          high = mid - 1;
        }
      }
      
      return result;
    }
  
    // Find the first and last occurrences of num
    const firstOccurrence = findFirstOccurrence(arr, num);
    const lastOccurrence = findLastOccurrence(arr, num);
  
    // If the number is not found, return -1
    if (firstOccurrence === -1 || lastOccurrence === -1) {
      return -1;
    }
  
    // Calculate and return the frequency
    return lastOccurrence - firstOccurrence + 1;
  }
  
  module.exports = sortedFrequency;