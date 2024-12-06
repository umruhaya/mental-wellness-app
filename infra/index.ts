import * as pulumi from "@pulumi/pulumi"
import * as gcp from "@pulumi/gcp"

// Configuration
const config = new pulumi.Config("gcp")
const projectId = config.require("project")
const domainName = "mentalwellness.umernaeem.com"

const region = "us-central1"
const zone = "us-central1-a"

const instanceName = "mental-wellness-app"
const machineType = "n1-standard-2"
const diskSize = 40 // in GB

const ipName = "mental-welness-lb-ip"
const firewallRuleName = "allow-http-https"
const loadBalancerName = "mental-welness-lb"

// Reserve a global static IP address
const staticIp = new gcp.compute.GlobalAddress(ipName, {
    project: projectId,
})

// Create a Compute Engine instance
const instance = new gcp.compute.Instance(instanceName, {
    project: projectId,
    zone: zone,
    machineType: machineType,
    bootDisk: {
        initializeParams: {
            image: "debian-cloud/debian-11",
            size: diskSize,
        },
    },
    networkInterfaces: [{
        network: "default",
        accessConfigs: [{}], // Ephemeral public IP
    }],
    tags: ["http-server", "https-server"],
})

// Allow firewall traffic on ports 80 and 443
const firewall = new gcp.compute.Firewall(firewallRuleName, {
    project: projectId,
    network: "default",
    allows: [
        { protocol: "tcp", ports: ["80", "443", "8000"] },
    ],
    sourceRanges: ["0.0.0.0/0"],
    targetTags: ["http-server", "https-server"],
})

const APP_PORT = 8000

// Create an unmanaged instance group
const instanceGroup = new gcp.compute.InstanceGroup(`${instanceName}-group`, {
    project: projectId,
    zone: zone,
    instances: [instance.selfLink],
    namedPorts: [
        {
            name: 'server',
            port: APP_PORT,
        },
    ],
})

// Create a health check
const healthCheck = new gcp.compute.HttpHealthCheck(`${loadBalancerName}-hc`, {
    project: projectId,
    port: APP_PORT,
    requestPath: "/health",
})

// Create a backend service
const backendService = new gcp.compute.BackendService(`${loadBalancerName}-backend`, {
    project: projectId,
    protocol: "HTTP",
    healthChecks: healthCheck.selfLink,
    backends: [{
        group: instanceGroup.selfLink,
    }],
    portName: "server",
    // provides Force HTTPS redirect
    // customResponseHeaders: [
    //     'Strict-Transport-Security:max-age=31536000;',
    //     'includeSubDomains; preload',
    // ]
})

// Create a URL map
const urlMap = new gcp.compute.URLMap(`${loadBalancerName}-url-map`, {
    project: projectId,
    defaultService: backendService.selfLink,
})

// Create a managed SSL certificate
const sslCertificate = new gcp.compute.ManagedSslCertificate(`${loadBalancerName}-cert`, {
    project: projectId,
    managed: {
        domains: [domainName],
    },
})

// Create target HTTPS proxy
const targetHttpsProxy = new gcp.compute.TargetHttpsProxy(`${loadBalancerName}-target-https-proxy`, {
    project: projectId,
    sslCertificates: [sslCertificate.selfLink],
    urlMap: urlMap.selfLink,
})

// Create target HTTP proxy
const targetHttpProxy = new gcp.compute.TargetHttpProxy(`${loadBalancerName}-target-http-proxy`, {
    project: projectId,
    urlMap: urlMap.selfLink,
})

// Create HTTPS forwarding rule
const forwardingRuleHttps = new gcp.compute.GlobalForwardingRule(`${loadBalancerName}-fr-https`, {
    project: projectId,
    ipAddress: staticIp.address,
    portRange: "443",
    target: targetHttpsProxy.selfLink,
})

// Create HTTP forwarding rule
const forwardingRuleHttp = new gcp.compute.GlobalForwardingRule(`${loadBalancerName}-fr-http`, {
    project: projectId,
    ipAddress: staticIp.address,
    portRange: "80",
    target: targetHttpProxy.selfLink,
})

// Output the IP address and instructions
export const ipAddress = staticIp.address
export const instructions = pulumi.interpolate`Provisioning complete. Please ensure your domain's DNS is updated to point to the IP address: ${ipAddress}. You can check the status of the SSL certificate with the following command:
gcloud compute ssl-certificates describe ${sslCertificate.name} --global --project ${projectId}`