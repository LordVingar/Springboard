function findRotatedIndex(arr, num) {
    // Helper function to find the pivot point
    function findPivot(arr) {
      let low = 0;
      let high = arr.length - 1;
  
      while (low <= high) {
        let mid = Math.floor((low + high) / 2);
  
        if (mid < high && arr[mid] > arr[mid + 1]) {
          return mid;
        }
        if (mid > low && arr[mid] < arr[mid - 1]) {
          return mid - 1;
        }
        if (arr[low] >= arr[mid]) {
          high = mid - 1;
        } else {
          low = mid + 1;
        }
      }
      return -1; // Array is not rotated
    }
  
    // Helper function to perform binary search
    function binarySearch(arr, low, high, num) {
      while (low <= high) {
        let mid = Math.floor((low + high) / 2);
  
        if (arr[mid] === num) {
          return mid;
        }
        if (arr[mid] < num) {
          low = mid + 1;
        } else {
          high = mid - 1;
        }
      }
      return -1; // Number not found
    }
  
    let pivot = findPivot(arr);
  
    // If no rotation, just perform binary search on the entire array
    if (pivot === -1) {
      return binarySearch(arr, 0, arr.length - 1, num);
    }
  
    // If the number is at the pivot
    if (arr[pivot] === num) {
      return pivot;
    }
  
    // Determine which half to search
    if (num >= arr[0] && num <= arr[pivot]) {
      return binarySearch(arr, 0, pivot, num);
    } else {
      return binarySearch(arr, pivot + 1, arr.length - 1, num);
    }
  }
  
  module.exports = findRotatedIndex;