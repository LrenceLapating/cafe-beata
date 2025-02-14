<template>
  <div class="policy-container">
    <h1>Privacy and Policy</h1>
    
    
    <p>Welcome to UIC Cafe Beàta. By using our services, you agree to abide by the following terms and conditions. Failure to comply may result in disciplinary actions.</p>
    
    <h2>1. Use of UIC Email</h2>
    <p>All users must register and log in using their official University of the Immaculate Conception email . Any attempt to use unauthorized email accounts for ordering will be strictly prohibited, and access may be revoked without notice.</p>
    
    <h2>2. Ordering Guidelines</h2>
    <ul>
      <li><strong>Order Confirmation:</strong> Once an order is placed, it is considered final. No modifications or cancellations will be entertained.</li>
      <li><strong>Order Pickup:</strong> Orders must be picked up within the designated time. Failure to do so will result in the order being forfeited and forwarded to OSAD for documentation.</li>
      <li><strong>Strict Compliance:</strong> Any student failing to collect their order repeatedly will face disciplinary measures, which may include account suspension or further academic penalties.</li>
    </ul>
    
    <h2>3. Payment and Refunds</h2>
    <ul>
      <li><strong>Payment Policy:</strong> All transactions must be completed through the approved payment methods. Failure to pay on time will result in order cancellation.</li>
      <li><strong>Refunds:</strong> Refunds will only be issued under special circumstances, such as system errors or unavailability of items.</li>
    </ul>
    
    <h2>4. Code of Conduct</h2>
    <ul>
      <li>Any form of <strong>misuse, fraudulent activities, or abuse of the ordering system</strong> will be taken seriously.</li>
      <li>Attempting to <strong>place fake orders</strong> or misuse someone else's UIC email for transactions will be reported to university authorities.</li>
      <li>Respect for cafe staff and adherence to pick-up schedules is mandatory. Any disrespectful behavior will result in immediate action.</li>
    </ul>
    
    <h2>5. Disciplinary Actions</h2>
    <ol>
      <li><strong>First Offense:</strong> Formal warning and documentation by OSAD.</li>
      <li><strong>Second Offense:</strong> Temporary suspension of ordering privileges.</li>
      <li><strong>Third Offense:</strong> Permanent ban from the UIC Cafe Beàta system, with further disciplinary actions taken by the university.</li>
    </ol>
    
    <h2>6. Changes to Policy</h2>
    <p>UIC Cafe Beàta reserves the right to amend these policies at any time. Users will be notified of any major changes.</p>
    
    <p>By continuing to use this service, you acknowledge that you have read, understood, and agreed to these terms. Failure to comply will result in strict enforcement of the stated guidelines.</p>
    
    <router-link to="/login" class="back-link">Back to Login</router-link>
  </div>
</template>


<script>
export default {
  name: "PrivacyAndPolicy",
};
</script>

<style scoped>





.policy-container {
  max-width: 600px;
  margin: 40px auto;
  padding: 20px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

h1, h2 {
  color:rgb(179, 49, 109);
}

.back-link {
  display: block;
  margin-top: 20px;
  color:rgb(192, 51, 157);
  text-decoration: none;
  font-weight: bold;
}

.back-link:hover {
  text-decoration: underline;
}
</style>
