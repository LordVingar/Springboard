function findRotationCount(arr) {
    let low = 0;
    let high = arr.length - 1;
  
    // If the array is not rotated at all
    if (arr[low] <= arr[high]) {
      return 0;
    }
  
    while (low <= high) {
      let mid = Math.floor((low + high) / 2);
  
      // Check if mid is the minimum element
      if (arr[mid] > arr[mid + 1]) {
        return mid + 1;
      }
      if (arr[mid] < arr[mid - 1]) {
        return mid;
      }
  
      // Decide which half to search
      if (arr[mid] >= arr[low]) {
        low = mid + 1;
      } else {
        high = mid - 1;
      }
    }
    return 0;
  }
  
  module.exports = findRotationCount;