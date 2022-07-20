const b = [3, 432, 1, 3, 2];

function f() {
  let j = 0;
  for (let i = 0; i < a.length; i++) {
    if (a[i] == b[j]) {
      j++;
      if (j == b.length - 1) {
        console.log("YES");
        return;
      }
    }
  }
  console.log("NOOOO");
}

// f();
const a = [-100, -73, -23, -3, 2, 10, 11, 69, 432];

function g() {
  let w = [];
  let j = a.length - 1;
  for (let i = 0; i < a.length; i++) {
    let c = a[i] ** 2;
    if (i == j) {
      w.unshift(c);
      return;
    }
    if (a[i] ** 2 < a[j] ** 2) {
      i--;
      let t = a[j] ** 2;
      w.unshift(t);
      j--;
    } else {
      w.unshift(c);
    }
  }
  console.log(w);
}

const go = [
  [1, 2],
  [2, 4],
  [2, 3],
  [2, 3],
  [4, 3],
  [1, 4],
];

const ar = [1, 0, 1, 0, 1, 0];

function r() {
  let h = [];
  for (let i = 0; i < ar.length; i++) {
    let objkey;
    if (ar[i] == 1) {
      objkey = go[i][0];
    } else {
      objkey = go[i][1];
    }
    let points = h.find((e) => {
      if (e.key == go[i][1]) {
        return go[i][1];
      }
    });
    // console.log(points.value);

    if (points) {
      let t = parseInt(points.value) + 3;
      h.filter((data) => data.key != points.key);

      let obj = { key: go[i][1], value: t };
      h.push(obj);
    } else {
      let obj = { key: go[i][1], value: 3 };
      h.push(obj);
    }
  }
}

r();
