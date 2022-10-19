let btns = document.getElementsByClassName("addtoCart");
for (let i = 0; i < btns.length; i++) {
  btns[i].addEventListener("click", function () {
    let productId = this.dataset.product;
    let action = this.dataset.action;

    if (user === "AnonymousUser") {
      addCookies(productId, action);
    } else {
      updateCart(productId, action);
    }
  });
}

function addCookies(id, action) {
  if (action == "add") {
    if (cart[id] == undefined) {
      cart[id] = { quantity: 1 };
    } else {
      cart[id]["quantity"] += 1;
    }
  }

  if (action == "remove") {
    cart[id]["quantity"] -= 1;
  }
  if (cart[id]["quantity"] <= 0) {
    delete cart[id];
  }
  console.log("Cart:", cart);
  document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/";
  location.reload();
}

function updateCart(id, action) {
  let url = "/update_Item/";
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ productId: id, action: action }),
  })
    .then((response) => response.json())
    .then((data) => {
      location.reload();
    });
}
