function findFloor(arr, num) {
    let low = 0;
    let high = arr.length - 1;
    let floor = -1;

    while (low <= high) {
        let mid = Math.floor((low + high) / 2);

        if (arr[mid] === num) {
            return arr[mid];
        } else if (arr[mid] < num) {
            floor = arr[mid];
            low = mid + 1;
        } else {
            high = mid - 1;
        }
    }

    return floor;
}

module.exports = findFloor;