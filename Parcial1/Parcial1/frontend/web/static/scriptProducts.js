// ---- Endpoints base ----
const PRODUCTS_BASE = "http://192.168.80.3:5003";
const ORDERS_BASE   = "http://192.168.80.3:5004";

// ---- Helpers ----
const json  = (r) => r.json();
const okJson = (r) => r.json().then((b) => ({ ok: r.ok, body: b }));

// ---- Listar productos ----
function getProducts() {
  fetch(`${PRODUCTS_BASE}/api/products`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
  })
    .then(json)
    .then((data) => {
      const tbody = document.querySelector("#product-list tbody");
      tbody.innerHTML = "";

      data.forEach((p) => {
        const tr = document.createElement("tr");

        tr.innerHTML = `
          <td>${p.id}</td>
          <td>${p.name}</td>
          <td>${p.price}</td>
          <td>${p.quantity}</td>
          <td><input type="text" value="0" class="form-control form-control-sm" style="width:110px"></td>
          <td>
            <a href="/editProduct/${p.id}" class="btn btn-primary btn-sm mr-2">Edit</a>
            <a href="#" class="btn btn-danger btn-sm js-del">Delete</a>
          </td>
        `;

        tr.querySelector(".js-del").addEventListener("click", (ev) => {
          ev.preventDefault();
          deleteProduct(p.id);
        });

        tbody.appendChild(tr);
      });
    })
    .catch((e) => console.error("getProducts error:", e));
}

// ---- Crear producto ----
function createProduct() {
  const data = {
    name:     document.getElementById("name").value,
    price:    document.getElementById("price").value,
    quantity: document.getElementById("quantity").value,
  };

  fetch(`${PRODUCTS_BASE}/api/products`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  })
    .then(okJson)
    .then(({ ok, body }) => {
      if (!ok) throw new Error(body.message || "Error creating product");
      getProducts();
      alert("Product created");
    })
    .catch((e) => alert(e.message));
}

// ---- Actualizar producto (form de edición) ----
function updateProduct() {
  const productId = document.getElementById("product-id").value;
  const data = {
    name:     document.getElementById("name").value,
    price:    document.getElementById("price").value,
    quantity: document.getElementById("quantity").value,
  };

  fetch(`${PRODUCTS_BASE}/api/products/${productId}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  })
    .then(okJson)
    .then(({ ok, body }) => {
      if (!ok) throw new Error(body.message || "Error updating product");
      alert("Product updated");
      window.location.href = "/products";
    })
    .catch((e) => alert(e.message));
}

// ---- Eliminar producto ----
function deleteProduct(productId) {
  if (!confirm("Are you sure you want to delete this product?")) return;

  fetch(`${PRODUCTS_BASE}/api/products/${productId}`, { method: "DELETE" })
    .then(okJson)
    .then(({ ok, body }) => {
      if (!ok) throw new Error(body.message || "Error deleting product");
      getProducts();
    })
    .catch((e) => alert(e.message));
}

// ---- Crear orden (descuenta inventario) ----
function orderProducts() {
  // Recolectar cantidades > 0 desde la tabla
  const selectedProducts = [];
  document.querySelectorAll("#product-list tbody tr").forEach((row) => {
    const id = parseInt(row.children[0].textContent, 10);
    const qty = parseInt(row.querySelector("input").value || "0", 10);
    if (qty > 0) selectedProducts.push({ id, quantity: qty });
  });

  if (selectedProducts.length === 0) {
    alert("Por favor, selecciona al menos un producto para realizar la orden.");
    return;
  }

  // Usuario desde sessionStorage (se guardan al loguearse)
  const userName  = sessionStorage.getItem("username");
  const userEmail = sessionStorage.getItem("email");

  const payload = {
    userName,
    userEmail,
    products: selectedProducts,
  };

  fetch(`${ORDERS_BASE}/api/orders`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify(payload),
  })
    .then(okJson)
    .then(({ ok, body }) => {
      if (!ok) throw new Error(body.message || "Error creating order");
      alert("¡Orden creada exitosamente!");
      // refrescar inventario y listado de órdenes
      getProducts();
      getOrders();
    })
    .catch((e) => {
      console.error("orderProducts error:", e);
      alert("Error al crear la orden. Por favor, intenta nuevamente.");
    });
}

// ---- Listar órdenes ----
function getOrders() {
  fetch(`${ORDERS_BASE}/api/orders`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
  })
    .then(json)
    .then((orders) => {
      const tbody = document.querySelector("#orders-table tbody");
      tbody.innerHTML = "";

      orders.forEach((o) => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td>${o.id}</td>
          <td>${o.userName}</td>
          <td>${o.userEmail}</td>
          <td>${o.saleTotal}</td>
          <td>${o.date}</td>
          <td><a class="btn btn-primary btn-sm" href="/order/${o.id}">View</a></td>
        `;
        tbody.appendChild(tr);
      });
    })
    .catch((e) => console.error("getOrders error:", e));
}

// ---- Exponer funciones globalmente para los onclick del HTML ----
window.getProducts   = getProducts;
window.createProduct = createProduct;
window.updateProduct = updateProduct;
window.deleteProduct = deleteProduct;
window.orderProducts = orderProducts;
window.getOrders     = getOrders;

// (opcional) auto-cargar productos al abrir la vista
document.addEventListener("DOMContentLoaded", () => {
  if (document.querySelector("#product-list")) getProducts();
});
