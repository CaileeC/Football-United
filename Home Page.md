# Football-United
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Football United</title>
    <link rel="stylesheet" href="styles.css" />
</head>
<body> 
    <header> 
        <div class="logo">
            <img src="images/logo.png" alt="Football United">
            <h1>Football United</h1>
        </div>
        <nav>
            <ul>
                <li><a href="#">Home</a></li> 
                <li><a href="#">Teams</a></li>   
                <li><a href="#">Pricing</a></li>
                <li><a href="#">Login</a></li>
            </ul>
        </nav>
    </header>
    <section class="hero">
        <h2>Stream Only the Teams You Love</h2>
        <p>Choose one team or combine your favorites. No more paying for every game, just what you care about.</p>
        <a href="#" class="cta-button">Get Started</a>
    </section>

</body>

</body>

<head>
  <meta charset="UTF-8" />
  <title>NFL Team Subscriptions — Checkout</title>
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <link rel="stylesheet" href="styles.css" />

  <style>
    body {
      font-family: Arial, sans-serif;
      background: #f9f9f9;
      padding: 20px;
    }

    table {
      border-collapse: collapse;
      width: 100%;
      max-width: 900px;
      margin: auto;
      box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    }

    th, td {
      padding: 10px;
      border: 1px solid #ddd;
      text-align: center;
      font-size: 14px;
    }

    th {
      background-color: #333;
      color: white;
      font-size: 16px;
    }

    tr.selected {
      outline: 3px solid #FFD700;
    }

    tr td input[type="checkbox"] {
      transform: scale(1.2);
      cursor: pointer;
    }

    /* Team Colors */
    .ARI { background:#97233F; color:#FFF; }
    .ATL { background:#A71930; color:#FFF; }
    .BAL { background:#241773; color:#FFF; }
    .BUF { background:#00338D; color:#FFF; }
    .CAR { background:#0085CA; color:#FFF; }
    .CHI { background:#0B162A; color:#FFF; }
    .CIN { background:#FB4F14; color:#000; }
    .CLE { background:#311D00; color:#FFF; }
    .DAL { background:#002244; color:#FFF; }
    .DEN { background:#002244; color:#FFF; }
    .DET { background:#0076B6; color:#FFF; }
    .GB  { background:#203731; color:#FFB612; }
    .HOU { background:#03202F; color:#FFF; }
    .IND { background:#002C5F; color:#FFF; }
    .JAX { background:#006778; color:#FFF; }
    .KC  { background:#E31837; color:#FFF; }
    .LV  { background:#000; color:#A5ACAF; }
    .LAC { background:#002A5E; color:#FFF; }
    .LAR { background:#003594; color:#FFC20E; }
    .MIA { background:#008E97; color:#F58220; }
    .MIN { background:#4F2683; color:#FFC62F; }
    .NE  { background:#002244; color:#C60C30; }
    .NO  { background:#D3BC8D; color:#101820; }
    .NYG { background:#0B2265; color:#A71930; }
    .NYJ { background:#125740; color:#FFF; }
    .PHI { background:#004C54; color:#FFF; }
    .PIT { background:#101820; color:#FFB612; }
    .SEA { background:#002244; color:#69BE28; }
    .SF  { background:#AA0000; color:#B3995D; }
    .TB  { background:#D50A0A; color:#FFF; }
    .TEN { background:#4B92DB; color:#FFF; }
    .WAS { background:#773141; color:#FFB612; }

    .site-header, .site-footer {
      background: #111;
      color: #fff;
      padding: 10px 0;
      margin-bottom: 20px;
    }

    .site-header .wrap,
    .site-footer .wrap,
    .checkout-grid.wrap,
    .wrap {
      max-width: 1100px;
      margin: 0 auto;
      padding: 0 10px;
    }

    .site-header nav a {
      color: #fff;
      margin-right: 15px;
      text-decoration: none;
    }

    .site-header nav a.active {
      text-decoration: underline;
    }

    .checkout-grid {
      display: grid;
      gap: 20px;
    }

    @media (min-width: 900px) {
      .checkout-grid {
        grid-template-columns: 2fr 1.5fr;
      }
    }

    .card {
      background: #fff;
      border-radius: 6px;
      padding: 15px;
      box-shadow: 0 1px 4px rgba(0,0,0,0.12);
    }

    .card-head {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
    }

    .btn {
      display: inline-block;
      padding: 6px 12px;
      border-radius: 4px;
      border: none;
      cursor: pointer;
      text-decoration: none;
      background: #333;
      color: #fff;
    }

    .btn.primary {
      font-weight: bold;
    }

    .table-wrap {
      overflow-x: auto;
      margin-bottom: 10px;
    }

    .row {
      margin-bottom: 10px;
    }

    .row.inline {
      display: flex;
      gap: 10px;
      align-items: flex-end;
    }

    .row.inline > div {
      flex: 1;
    }

    .inline {
      display: flex;
      gap: 10px;
      align-items: center;
    }

    input, select {
      width: 100%;
      padding: 6px;
      box-sizing: border-box;
    }

    .muted {
      font-size: 0.85em;
      color: #555;
    }

    .totals {
      border-top: 1px solid #ddd;
      padding-top: 10px;
      margin-top: 10px;
    }

    .totals-row {
      display: flex;
      justify-content: space-between;
      margin-bottom: 4px;
    }

    .totals-row.grand {
      font-weight: bold;
      border-top: 1px solid #ddd;
      padding-top: 6px;
      margin-top: 6px;
    }
  </style>

  <script defer src="app.js"></script>
</head>
<body>
  <header class="site-header">
    <div class="wrap">
      <h1>NFL Subscriptions</h1>
      <nav>
        <a href="index.html">Home</a>
        <a href="subscribe.html">Subscribe</a>
        <a href="checkout.html" class="active">Checkout</a>
      </nav>
    </div>
  </header>

  <main class="wrap checkout-grid">
    <section class="card">
      <h2 style="text-align: center;">NFL Team Subscriptions</h2>
      <table id="teamTable">
        <thead>
          <tr>
            <th>Select</th>
            <th>Team</th>
            <th>Price</th>
          </tr>
        </thead>
        <tbody>
          <tr class="ARI"><td><input type="checkbox"></td><td>Arizona Cardinals</td><td>$14.99</td></tr>
          <tr class="ATL"><td><input type="checkbox"></td><td>Atlanta Falcons</td><td>$14.99</td></tr>
          <tr class="BAL"><td><input type="checkbox"></td><td>Baltimore Ravens</td><td>$14.99</td></tr>
          <tr class="BUF"><td><input type="checkbox"></td><td>Buffalo Bills</td><td>$14.99</td></tr>
          <tr class="CAR"><td><input type="checkbox"></td><td>Carolina Panthers</td><td>$14.99</td></tr>
          <tr class="CHI"><td><input type="checkbox"></td><td>Chicago Bears</td><td>$14.99</td></tr>
          <tr class="CIN"><td><input type="checkbox"></td><td>Cincinnati Bengals</td><td>$14.99</td></tr>
          <tr class="CLE"><td><input type="checkbox"></td><td>Cleveland Browns</td><td>$14.99</td></tr>
          <tr class="DAL"><td><input type="checkbox"></td><td>Dallas Cowboys</td><td>$14.99</td></tr>
          <tr class="DEN"><td><input type="checkbox"></td><td>Denver Broncos</td><td>$14.99</td></tr>
          <tr class="DET"><td><input type="checkbox"></td><td>Detroit Lions</td><td>$14.99</td></tr>
          <tr class="GB"><td><input type="checkbox"></td><td>Green Bay Packers</td><td>$14.99</td></tr>
          <tr class="HOU"><td><input type="checkbox"></td><td>Houston Texans</td><td>$14.99</td></tr>
          <tr class="IND"><td><input type="checkbox"></td><td>Indianapolis Colts</td><td>$14.99</td></tr>
          <tr class="JAX"><td><input type="checkbox"></td><td>Jacksonville Jaguars</td><td>$14.99</td></tr>
          <tr class="KC"><td><input type="checkbox"></td><td>Kansas City Chiefs</td><td>$14.99</td></tr>
          <tr class="LV"><td><input type="checkbox"></td><td>Las Vegas Raiders</td><td>$14.99</td></tr>
          <tr class="LAC"><td><input type="checkbox"></td><td>Los Angeles Chargers</td><td>$14.99</td></tr>
          <tr class="LAR"><td><input type="checkbox"></td><td>Los Angeles Rams</td><td>$14.99</td></tr>
          <tr class="MIA"><td><input type="checkbox"></td><td>Miami Dolphins</td><td>$14.99</td></tr>
          <tr class="MIN"><td><input type="checkbox"></td><td>Minnesota Vikings</td><td>$14.99</td></tr>
          <tr class="NE"><td><input type="checkbox"></td><td>New England Patriots</td><td>$14.99</td></tr>
          <tr class="NO"><td><input type="checkbox"></td><td>New Orleans Saints</td><td>$14.99</td></tr>
          <tr class="NYG"><td><input type="checkbox"></td><td>New York Giants</td><td>$14.99</td></tr>
          <tr class="NYJ"><td><input type="checkbox"></td><td>New York Jets</td><td>$14.99</td></tr>
          <tr class="PHI"><td><input type="checkbox"></td><td>Philadelphia Eagles</td><td>$14.99</td></tr>
          <tr class="PIT"><td><input type="checkbox"></td><td>Pittsburgh Steelers</td><td>$14.99</td></tr>
          <tr class="SEA"><td><input type="checkbox"></td><td>Seattle Seahawks</td><td>$14.99</td></tr>
          <tr class="SF"><td><input type="checkbox"></td><td>San Francisco 49ers</td><td>$14.99</td></tr>
          <tr class="TB"><td><input type="checkbox"></td><td>Tampa Bay Buccaneers</td><td>$14.99</td></tr>
          <tr class="TEN"><td><input type="checkbox"></td><td>Tennessee Titans</td><td>$14.99</td></tr>
          <tr class="WAS"><td><input type="checkbox"></td><td>Washington Commanders</td><td>$14.99</td></tr>
        </tbody>
      </table>
    </section>

    <section class="card">
      <div class="card-head">
        <h2>Your Cart</h2>
        <a class="btn" href="subscribe.html">Edit Selections</a>
      </div>

      <div class="table-wrap">
        <table id="cartTable">
          <thead>
            <tr>
              <th>Team</th>
              <th>Price (mo)</th>
              <th></th>
            </tr>
          </thead>
          <tbody id="cartBody"></tbody>
        </table>
      </div>

      <div class="row">
        <label for="billingCycle"><strong>Billing cycle</strong></label>
        <select id="billingCycle">
          <option value="monthly">Monthly</option>
          <option value="annual">Annual (10% off)</option>
        </select>
      </div>

      <div class="row">
        <label for="promo"><strong>Promo code</strong></label>
        <div class="inline">
          <input id="promo" placeholder="Enter code (try NFL10)" />
          <button class="btn" id="applyPromo">Apply</button>
        </div>
      </div>

      <div class="totals" id="totalsBox"></div>

      <hr />

      <h2>Payment Details</h2>
      <form id="payForm" novalidate>
        <div class="row">
          <label>Full name</label>
          <input id="fullName" required placeholder="e.g., Taylor Smith" />
        </div>

        <div class="row">
          <label>Email (for receipts &amp; alerts)</label>
          <input id="email" type="email" required placeholder="you@example.com" />
        </div>

        <div class="row">
          <label>Card number</label>
          <input id="cardNum" inputmode="numeric" maxlength="19" placeholder="4111 1111 1111 1111" required />
        </div>

        <div class="row inline">
          <div>
            <label>Expiry (MM/YY)</label>
            <input id="exp" placeholder="12/29" required />
          </div>
          <div>
            <label>CVV</label>
            <input id="cvv" inputmode="numeric" maxlength="4" placeholder="123" required />
          </div>
        </div>

        <div class="row">
          <label>
            <input type="checkbox" id="agree" />
            I agree to recurring billing (cancel anytime).
          </label>
        </div>

        <button class="btn primary" type="submit" id="payBtn">Pay Now</button>
      </form>
    </section>
  </main>

  <footer class="site-footer">
    <div class="wrap">
      <small>&copy; 2025 NFL Subscriptions. All rights reserved.</small>
    </div>
  </footer>

  <script>
    document.querySelectorAll('#teamTable tbody tr').forEach(row => {
      const cb = row.querySelector('input[type="checkbox"]');
      cb.addEventListener('change', () => {
        row.classList.toggle('selected', cb.checked);
      });
    });
  </script>

  <script>
    document.addEventListener('DOMContentLoaded', () => {
      renderCartTable('cartBody', onRemoveItem);
      refreshTotals();

      document.getElementById('billingCycle').addEventListener('change', refreshTotals);
      document.getElementById('applyPromo').addEventListener('click', () => {
        const code = document.getElementById('promo').value.trim().toUpperCase();
        setPromo(code || null);
        refreshTotals();
      });

      document.getElementById('payForm').addEventListener('submit', (e) => {
        e.preventDefault();
        if (!validatePaymentForm()) return;
        const order = buildOrderSummary();
        localStorage.setItem('lastOrder', JSON.stringify(order));
        window.location.href = 'success.html';
      });
    });
  </script>
</body>

</html>