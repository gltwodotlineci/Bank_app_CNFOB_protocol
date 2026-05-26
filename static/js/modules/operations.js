// const bankSelect = document.getElementById("bank-select");
// const accountSelect = document.getElementById("account-select");
// const operationsBody = document.getElementById("operations-body");

// let allOperations = [];
// let currentBankId = null;
// let currentAccountId = null;

// /* =========================
//    LOAD BANKS
// ========================= */
// async function loadBanks() {
//     try {
//         const response = await fetch("/api/banks/");
//         const banks = await response.json();

//         bankSelect.innerHTML = `<option value="">-- Select Bank --</option>`;

//         banks.forEach(bank => {
//             bankSelect.innerHTML += `
//                 <option value="${bank.id}">
//                     ${bank.name}
//                 </option>
//             `;
//         });

//     } catch (error) {
//         console.error(error);

//         bankSelect.innerHTML = `
//             <option value="">
//                 Error loading banks
//             </option>
//         `;
//     }
// }

// /* =========================
//    LOAD ACCOUNTS
// ========================= */
// async function loadAccounts(bankId) {
//     accountSelect.innerHTML = `<option value="">Loading...</option>`;

//     try {
//         const response = await fetch(`/api/banks/${bankId}/accounts/`);
//         const accounts = await response.json();

//         accountSelect.innerHTML = `<option value="">All</option>`;

//         accounts.forEach(account => {
//             accountSelect.innerHTML += `
//                 <option value="${account.id}">
//                     ${account.number}
//                 </option>
//             `;
//         });

//     } catch (error) {
//         console.error(error);

//         accountSelect.innerHTML = `
//             <option value="">
//                 Error loading accounts
//             </option>
//         `;
//     }
// }

// /* =========================
//    LOAD OPERATIONS
// ========================= */
// async function loadOperations(bankId, accountId) {
//     operationsBody.innerHTML = `
//         <tr>
//             <td colspan="8" class="text-center">
//                 Loading...
//             </td>
//         </tr>
//     `;

//     try {
//         const response = await fetch(
//             `/api/banks/${bankId}/accounts/${accountId}/operations/`
//         );

//         const operations = await response.json();

//         allOperations = operations;

//         renderOperations(allOperations);

//     } catch (error) {
//         console.error(error);

//         operationsBody.innerHTML = `
//             <tr>
//                 <td colspan="8"
//                     class="text-center text-danger py-4">
//                     Error loading operations
//                 </td>
//             </tr>
//         `;
//     }
// }

// /* =========================
//    RENDER TABLE
// ========================= */
// function renderOperations(operations) {
//     operationsBody.innerHTML = "";

//     if (!operations.length) {
//         operationsBody.innerHTML = `
//             <tr>
//                 <td colspan="8"
//                     class="text-center text-muted py-4">
//                     No operations found
//                 </td>
//             </tr>
//         `;
//         return;
//     }

//     operations.forEach(operation => {
//         operationsBody.innerHTML += `
//             <tr>

//                 <td>${operation.date || ""}</td>
//                 <td>${operation.label || ""}</td>

//                 <td class="text-end text-success fw-bold">
//                     ${operation.credit_or_debit === "C" ? operation.amount : ""}
//                 </td>

//                 <td class="text-end text-danger fw-bold">
//                     ${operation.credit_or_debit === "D" ? operation.amount : ""}
//                 </td>

//                 <td class="text-end">
//                     ${operation.credit_or_debit === "N" ? operation.amount : ""}
//                 </td>

//                 <td class="text-center">
//                     <input
//                         type="checkbox"
//                         class="form-check-input operation-checkbox"
//                         data-id="${operation.id}"
//                         ${operation.pointed ? "checked" : ""}
//                     >
//                 </td>

//                 <td>${operation.date_pointed || ""}</td>
//                 <td>${operation.pointer || ""}</td>

//             </tr>
//         `;
//     });
// }

// /* =========================
//    FILTER RADIO BUTTONS
// ========================= */
// function setupFilters() {

//     document.querySelectorAll("input[name='pointage']")
//         .forEach(radio => {

//             radio.addEventListener("change", function () {

//                 if (this.value === "all") {
//                     renderOperations(allOperations);
//                     return;
//                 }

//                 const filtered = allOperations.filter(op => {

//                     const isPointed = op.pointed === true;

//                     if (this.value === "pointed") {
//                         return isPointed;
//                     }

//                     if (this.value === "non_pointed") {
//                         return !isPointed;
//                     }

//                     return true;
//                 });

//                 renderOperations(filtered);
//             });
//         });
// }

// /* =========================
//    PATCH CHECKBOX (POINTING)
// ========================= */
// document.addEventListener("change", async function (event) {

//     if (!event.target.classList.contains("operation-checkbox")) return;

//     const checkbox = event.target;
//     const operationId = checkbox.dataset.id;

//     const previousState = !checkbox.checked;

//     try {
//         const response = await fetch(
//             `/api/banks/${currentBankId}/accounts/${currentAccountId}/operations/${operationId}/`,
//             {
//                 method: "PATCH",
//                 headers: {
//                     "Content-Type": "application/json",
//                     "X-CSRFToken": getCookie("csrftoken")
//                 },
//                 body: JSON.stringify({
//                     pointed: checkbox.checked
//                 })
//             }
//         );

//         const updated = await response.json();

//         const op = allOperations.find(o => o.id === operationId);

//         if (op) {
//             op.pointed = updated.pointed;
//             op.date_pointed = updated.date_pointed;
//             op.pointer = updated.pointer;
//         }

//         renderOperations(allOperations);

//     } catch (error) {
//         console.error(error);
//         checkbox.checked = previousState;
//     }
// });

// /* =========================
//    EVENTS: BANK / ACCOUNT
// ========================= */
// bankSelect.addEventListener("change", function () {

//     currentBankId = this.value;

//     accountSelect.innerHTML = `<option value="">All</option>`;
//     operationsBody.innerHTML = "";

//     if (!currentBankId) return;

//     loadAccounts(currentBankId);
// });

// accountSelect.addEventListener("change", function () {

//     currentAccountId = this.value;

//     if (!currentBankId || !currentAccountId) return;

//     loadOperations(currentBankId, currentAccountId);
// });

// /* =========================
//    INIT
// ========================= */
// document.addEventListener("DOMContentLoaded", function () {
//     loadBanks();
//     setupFilters();
// });

// /* =========================
//    CSRF
// ========================= */
// function getCookie(name) {
//     const match = document.cookie.match(
//         new RegExp("(^| )" + name + "=([^;]+)")
//     );
//     return match ? decodeURIComponent(match[2]) : null;
// }
