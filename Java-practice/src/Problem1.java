/*
Write a method that takes a List<Employee> as input and returns a Map<String, Employee>.

Using only Java 8 Streams (no traditional for or while loops), implement the following logic in a single pipeline if possible:

Find the highest-paid employee in each department.

Filter the result: Only include departments where the average salary of all employees in that department is strictly greater than 50,000.
 */

import java.util.*;
import java.util.stream.Collectors;

public class Problem1 {
    static void main() {
        List<Employee> employees = Arrays.asList(
                new Employee(1, "Alice", "Engineering", 80000),
                new Employee(2, "Bob", "Engineering", 60000),
                new Employee(3, "Charlie", "Engineering", 45000),

                new Employee(4, "David", "HR", 55000),
                new Employee(5, "Eve", "HR", 40000),
                new Employee(6, "Frank", "HR", 45000),

                new Employee(7, "Grace", "Sales", 90000),
                new Employee(8, "Heidi", "Sales", 50000),
                new Employee(9, "Ivan", "Sales", 55000)
        );

        getTopEmployeesInHighEarningDepts(employees);
    }

    static Map<String, Employee> getTopEmployeesInHighEarningDepts (List<Employee> employees) {
        // 1. Grouping the employees by dept
//        Map<String, List<Employee>> employeesByDept = employees.stream()
//                .collect(Collectors.groupingBy(Employee::getDepartment));
//
//        System.out.println(employeesByDept);

        // 2. Finding the average salary of that department in which the employees are present
        Map<String, Double> avgSalaryByDept = employees.stream()
                .collect(Collectors.groupingBy(Employee::getDepartment, Collectors.averagingDouble(Employee::getSalary)));
        System.out.println(avgSalaryByDept);

        // 3. Filtering only departments where average salary of the department is greater than 80000
        Map<String, Double> selectedDepartments =  avgSalaryByDept.entrySet().stream()
                .filter(entry -> entry.getValue() > 50000)
                .collect(Collectors.toMap(Map.Entry::getKey, Map.Entry::getValue));
        System.out.println(selectedDepartments);

        // 4. the highest-paid employee in each department.
        Map<String, Employee> highestPaidEmployeeByDept = employees.stream()
                .collect(Collectors.groupingBy(Employee::getDepartment))
                .entrySet().stream()
                .filter(entry -> selectedDepartments.containsKey(entry.getKey()))
                .collect(Collectors.toMap(Map.Entry::getKey, entry -> Collections.max(entry.getValue(), Comparator.comparingDouble(Employee::getSalary))));

        return highestPaidEmployeeByDept;
    }
}

class Employee {
    private int id;
    private String name;
    private String department;
    private double salary;

    public Employee(int id, String name, String department, double salary) {
        this.id = id;
        this.name = name;
        this.department = department;
        this.salary = salary;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getDepartment() {
        return department;
    }

    public void setDepartment(String department) {
        this.department = department;
    }

    public double getSalary() {
        return salary;
    }

    public void setSalary(double salary) {
        this.salary = salary;
    }

    @Override
    public String toString() {
        return "Employee{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", department='" + department + '\'' +
                ", salary=" + salary +
                '}';
    }
}