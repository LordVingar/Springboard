/** Node: node for a singly linked list. */
class Node {
  constructor(val) {
    this.val = val;
    this.next = null;
  }
}

/** LinkedList: chained together nodes. */
class LinkedList {
  constructor(vals = []) {
    this.head = null;
    this.tail = null;
    this.length = 0;

    for (let val of vals) this.push(val);
  }

  /** push(val): add new value to end of list. */
  push(val) {
    let newNode = new Node(val);

    if (!this.head) {
      this.head = newNode;
      this.tail = newNode;
    } else {
      this.tail.next = newNode;
      this.tail = newNode;
    }

    this.length += 1;
  }

  /** unshift(val): add new value to start of list. */
  unshift(val) {
    let newNode = new Node(val);

    if (!this.head) {
      this.head = newNode;
      this.tail = newNode;
    } else {
      newNode.next = this.head;
      this.head = newNode;
    }

    this.length += 1;
  }

  /** pop(): return & remove last item. */
  pop() {
    if (!this.head) throw new Error("List is empty");

    let current = this.head;
    let newTail = current;

    while (current.next) {
      newTail = current;
      current = current.next;
    }

    this.tail = newTail;
    this.tail.next = null;
    this.length -= 1;

    if (this.length === 0) {
      this.head = null;
      this.tail = null;
    }

    return current.val;
  }

  /** shift(): return & remove first item. */
  shift() {
    if (!this.head) throw new Error("List is empty");

    let current = this.head;
    this.head = this.head.next;
    this.length -= 1;

    if (this.length === 0) {
      this.tail = null;
    }

    return current.val;
  }

  /** getAt(idx): get val at idx. */
  getAt(idx) {
    if (idx < 0 || idx >= this.length) throw new Error("Invalid index");

    let current = this.head;
    let count = 0;

    while (count !== idx) {
      current = current.next;
      count += 1;
    }

    return current.val;
  }

  /** setAt(idx, val): set val at idx to val */
  setAt(idx, val) {
    if (idx < 0 || idx >= this.length) throw new Error("Invalid index");

    let current = this.head;
    let count = 0;

    while (count !== idx) {
      current = current.next;
      count += 1;
    }

    current.val = val;
  }

  /** insertAt(idx, val): add node w/val before idx. */
  insertAt(idx, val) {
    if (idx < 0 || idx > this.length) throw new Error("Invalid index");

    if (idx === 0) return this.unshift(val);
    if (idx === this.length) return this.push(val);

    let newNode = new Node(val);
    let current = this.head;
    let count = 0;

    while (count !== idx - 1) {
      current = current.next;
      count += 1;
    }

    newNode.next = current.next;
    current.next = newNode;
    this.length += 1;
  }

  /** removeAt(idx): return & remove item at idx, */
  removeAt(idx) {
    if (idx < 0 || idx >= this.length) throw new Error("Invalid index");

    if (idx === 0) return this.shift();
    if (idx === this.length - 1) return this.pop();

    let current = this.head;
    let count = 0;

    while (count !== idx - 1) {
      current = current.next;
      count += 1;
    }

    let removed = current.next;
    current.next = removed.next;
    this.length -= 1;

    return removed.val;
  }

  /** average(): return an average of all values in the list */
  average() {
    if (this.length === 0) return 0;

    let sum = 0;
    let current = this.head;

    while (current) {
      sum += current.val;
      current = current.next;
    }

    return sum / this.length;
  }
}

module.exports = LinkedList;
