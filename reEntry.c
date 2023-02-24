#include <stdio.h>
#include <math.h>

#define PI 3.14159265358979323846

// Constants
const double g = 9.81;  // acceleration due to gravity (m/s^2)
const double Cd = 0.47;  // drag coefficient
const double rho = 1.2;  // density of air (kg/m^3)
const double m = 150;  // mass of ball (kg)
const double r = 0.5;  // radius of ball (m)
const double A = PI * r * r;  // cross-sectional area of ball (m^2)
const double v0 = 100;  // initial velocity (m/s)
const double theta = PI / 4;  // launch angle (radians)
const double x0 = 0;  // initial position (m)
const double y0 = 10000;  // initial altitude (m)

int main() {
    // Time variables
    double t, dt;
    const double t_end = 100;
    const int n_steps = 10000;

    // Velocity variables
    double vx, vy, v;
    const double vx0 = v0 * cos(theta);
    const double vy0 = v0 * sin(theta);

    // Position variables
    double x, y;
    const double x_end = 1000000;

    // Terminal velocity
    const double vterm = sqrt(2 * m * g / (rho * Cd * A));

    // Impact time and velocity
    double t_impact, v_impact;

    // Open output file
    FILE *fp;
    fp = fopen("reentry.dat", "w");
    if (fp == NULL) {
        printf("Error opening output file.\n");
        return 1;
    }

    // Initial conditions
    t = 0;
    x = x0;
    y = y0;
    vx = vx0;
    vy = vy0;

    // Time step
    dt = t_end / n_steps;

    // Loop over time steps
    for (int i = 0; i < n_steps; i++) {
        // Calculate drag force
        double Fd = 0.5 * Cd * rho * A * v * v;

        // Calculate acceleration
        double ax = -Fd * vx / (m * v);
        double ay = -g - Fd * vy / (m * v);

        // Update velocity
        vx += ax * dt;
        vy += ay * dt;
        v = sqrt(vx * vx + vy * vy);

        // Update position
        x += vx * dt;
        y += vy * dt;

        // Check for impact
        if (y <= 0) {
            t_impact = t + dt * (-y) / (vy - sqrt(vy * vy - 2 * g * y));
            v_impact = sqrt(vx * vx + (vterm * tanh(t_impact * sqrt(g * rho * Cd * A / (2 * m)))) * (vterm * tanh(t_impact * sqrt(g * rho * Cd * A / (2 * m)))));
            break;
        }

        // Print output
        fprintf(fp, "%.2f\t%.2f\t%.2f\t%.2f\n", t, x, y, v);

        // Update time
        t += dt;

        // Stop if we've reached the end of the simulation
        if (x >= x
