// --- Endpoints ---
const PRODUCTS_BASE = "http://192.168.80.3:5003";
const ORDERS_BASE   = "http://192.168.80.3:5004";

// --- Helpers ---
const json = (r) => r.json();
const okJson = (r) => r.json().then((b) => ({ ok: r.ok, body: b }));

// --- Listar productos ---
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

      data.forEach((product) => {
        const tr = document.createElement("tr");

        // id
        const tdId = document.createElement("td");
        tdId.textContent = product.id;
        tr.appendChild(tdId);

        // name
        const tdName = document.createElement("td");
        tdName.textContent = product.name;
        tr.appendChild(tdName);

        // price
        const tdPrice = document.createElement("td");
        tdPrice.textContent = product.price;
        tr.appendChild(tdPrice);

        // quantity (stock)
        const tdStock = document.createElement("td");
        tdStock.textContent = product.quantity;
        tr.appendChild(tdStock);

        // order quantity (input)
        const tdOrderQty = document.createElement("td");
        const inp = document.createElement("input");
        inp.type = "number";
        inp.min = "0";
        inp.value = "0";
        inp.className = "order-qty";
        inp.setAttribute("data-product-id", product.id);
        tdOrderQty.appendChild(inp);
        tr.appendChild(tdOrderQty);

        // actions
        const tdActions = document.createElement("td");

        const edit = document.createElement("a");
        edit.href = `/editProduct/${product.id}`;
        edit.textContent = "Edit";
        edit.className = "btn btn-primary btn-sm mr-2";
        tdActions.appendChild(edit);

        const del = document.createElement("a");
        del.href = "#";
        del.textContent = "Delete";
        del.className = "btn btn-danger btn-sm";
        del.addEventListener("click", () => deleteProduct(product.id));
        tdActions.appendChild(del);

        tr.appendChild(tdActions);
        tbody.appendChild(tr);
      });
    })
    .catch((err) => console.error("getProducts error:", err));
}

// --- Crear producto ---
function createProduct() {
  const data = {
    name: document.getElementById("name").value,
    price: document.getElementById("price").value,
    quantity: document.getElementById("quantity").value,
  };

  fetch(`${PRODUCTS_BASE}/api/products`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  })
    .then(okJson)
    .then(({ ok, body }) => {
      if (!ok) throw new Error(body.message || "createProduct failed");
      getProducts();
      // limpiar form
      document.getElementById("name").value = "";
      document.getElementById("price").value = "";
      document.getElementById("quantity").value = "";
    })
    .catch((err) => console.error("createProduct error:", err));
}

// --- Borrar producto ---
function deleteProduct(productId) {
  if (!confirm("Are you sure you want to delete this product?")) return;

  fetch(`${PRODUCTS_BASE}/api/products/${productId}`, { method: "DELETE" })
    .then(okJson)
    .then(({ ok, body }) => {
      if (!ok) throw new Error(body.message || "deleteProduct failed");
      getProducts();
    })
    .catch((err) => console.error("deleteProduct error:", err));
}

// --- Crear orden ---
function orderProducts() {
  const selectedProducts = [];
  document.querySelectorAll('#product-list tbody tr').forEach(row => {
    const q = parseInt(row.querySelector('input[type="text"]').value || '0', 10);
    if (q > 0) {
      const pid = row.querySelector('td:nth-child(1)').textContent.trim();
      selectedProducts.push({ id: Number(pid), quantity: q });
    }
  });

  if (selectedProducts.length === 0) {
    alert('Por favor, selecciona al menos un producto para realizar la orden.');
    return;
  }

  const userName  = sessionStorage.getItem('username') || localStorage.getItem('username') || '';
  const userEmail = sessionStorage.getItem('email')    || localStorage.getItem('email')    || '';

  const payload = {
    user: { name: userName, email: userEmail },
    products: selectedProducts
  };

  console.log('[orderProducts] payload:', payload);

  fetch('http://192.168.80.3:5004/api/orders', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-User-Name': userName,
      'X-User-Email': userEmail
    },
    body: JSON.stringify(payload),
    credentials: 'include'
  })
  .then(r => r.json().then(j => ({ ok: r.ok, j })))
  .then(({ ok, j }) => {
    if (!ok) throw new Error(j.message || 'Error creando la orden');
    alert('¡Orden creada exitosamente!');
    // refresca productos y órdenes si quieres:
    if (typeof getProducts === 'function') getProducts();
    if (typeof getOrders === 'function') getOrders();
  })
  .catch(err => {
    console.error('orderProducts error:', err);
    alert(`Error al crear la orden: ${err.message}`);
  });
}
// --- Listar órdenes ---
function getOrders() {
  fetch(`${ORDERS_BASE}/api/orders`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
  })
    .then(json)
    .then((data) => {
      const tbody = document.querySelector("#order-list tbody");
      if (!tbody) return; // por si esta tabla no existe en otras páginas

      tbody.innerHTML = "";
      data.forEach((o) => {
        const tr = document.createElement("tr");

        const tdId = document.createElement("td");
        tdId.textContent = o.id;
        tr.appendChild(tdId);

        const tdUser = document.createElement("td");
        tdUser.textContent = o.userName;
        tr.appendChild(tdUser);

        const tdEmail = document.createElement("td");
        tdEmail.textContent = o.userEmail;
        tr.appendChild(tdEmail);

        const tdTotal = document.createElement("td");
        tdTotal.textContent = o.saleTotal;
        tr.appendChild(tdTotal);

        const tdDate = document.createElement("td");
        try { tdDate.textContent = new Date(o.date).toLocaleString(); }
        catch { tdDate.textContent = o.date; }
        tr.appendChild(tdDate);

        const tdActions = document.createElement("td");
        const viewBtn = document.createElement("button");
        viewBtn.className = "btn btn-primary btn-sm";
        viewBtn.textContent = "View";
        viewBtn.onclick = () => viewOrder(o.id);
        tdActions.appendChild(viewBtn);
        tr.appendChild(tdActions);

        tbody.appendChild(tr);
      });
    })
    .catch((err) => console.error("getOrders error:", err));
}

// --- Ver detalle simple de una orden ---
function viewOrder(orderId) {
  fetch(`${ORDERS_BASE}/api/orders/${orderId}`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
  })
    .then(json)
    .then((o) => {
      alert(
        `Order #${o.id}\n` +
        `User: ${o.userName}\n` +
        `Email: ${o.userEmail}\n` +
        `Total: ${o.saleTotal}\n` +
        `Date: ${o.date}`
      );
    })
    .catch((err) => console.error("viewOrder error:", err));
}

// Cargar listas al abrir la página
document.addEventListener("DOMContentLoaded", () => {
  getProducts();
  getOrders();
});
