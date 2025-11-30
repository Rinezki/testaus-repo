# 3.1 pt1 Integration Testing Report

## 1. General Information
- **Project:**  
- **Test Scope (modules/services):**  
- **Test Date:**  
- **Tester:**  
- **Version / Build:**  

---

## 2. Test Objective
Briefly describe the purpose of the integration testing:
- What needs to be verified?  
- Which interfaces, services, or components are involved?  

---

## 3. Test Environment
- **Platform:** (e.g., Proxmox, Docker, K3s, physical device)  
- **Operating System and Version:**  
- **Network Configuration:** (IPv4/IPv6, VLAN, firewall rules)  
- **Test Data / Mocks:**  

---

## 4. Test Scenarios
| ID | Description | Preconditions | Steps | Expected Result | Actual Result | Status |
|----|-------------|---------------|-------|----------------|---------------|--------|
| T1 | REST API call → database | DB running | Send POST /api/data | 200 OK + data stored | 200 OK | ✅ |
| T2 | MQTT message → HMI update | Broker running | Publish topic `sensor/temp` | HMI updates | No update | ❌ |

---

## 5. Test Results
- **Successful Tests:**  
- **Failed Tests:**  
- **Critical Issues:**  
- **Notes and Deviations:**  

---

## 6. Logs and Attachments
- **Log Files:** (paths, excerpts)  
- **Screenshots / Diagrams:**  
- **Additional Notes:**  

---

## 7. Conclusions
- Summary of successes and issues  
- Recommendations for next steps (bug fixes, additional tests, regression testing)  

---

## 8. Approval
- **Tester:**  
- **Project Manager / QA:**  
- **Date:**  