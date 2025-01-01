import * as pulumi from "@pulumi/pulumi"
import * as gcp from "@pulumi/gcp"

// Configuration
const config = new pulumi.Config("gcp")
const projectId = config.require("project")
const domainName = "mentalwellness.umernaeem.com"

const region = "us-central1"
const zone = "us-central1-a"

const instanceName = "mental-wellness-app"
const machineType = "e2-medium"
const diskSize = 40 // in GB

const ipName = "mental-welness-lb-ip"
const firewallRuleName = "allow-http-https"

const reservedIp = new gcp.compute.Address(ipName, {
    project: projectId,
    name: "mental-wellness-app",
    networkTier: "PREMIUM",
    region,
})

// Create a Compute Engine instance
const instance = new gcp.compute.Instance(instanceName, {
    name: "mental-wellness-app",
    project: projectId,
    zone: zone,
    machineType: machineType,
    bootDisk: {
        initializeParams: {
            // image: "debian-cloud/debian-11",
            image: "ubuntu-os-cloud/ubuntu-2204-lts",
            size: diskSize,
        },
    },
    networkInterfaces: [{
        network: "default",
        accessConfigs: [{
            natIp: reservedIp.address,
        }], // Ephemeral public IP
    }],
    tags: ["http-server", "https-server"],
})

// Allow firewall traffic on ports 80 and 443
const firewall = new gcp.compute.Firewall(firewallRuleName, {
    project: projectId,
    network: "default",
    allows: [
        { protocol: "tcp", ports: ["80", "443", "8000", "3000"] },
    ],
    sourceRanges: ["0.0.0.0/0"],
    targetTags: ["http-server", "https-server"],
})

// Output the IP address and instructions
export const ipAddress = reservedIp.address
export const instructions = pulumi.interpolate`Provisioning complete. Please ensure your domain's DNS is updated to point to the IP address: ${ipAddress}.`