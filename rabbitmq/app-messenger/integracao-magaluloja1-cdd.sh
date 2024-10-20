#!/bin/bash
#########################################################################################################################################################
# Magaluloja1 Communication Protocol Setup                                                                                                            #
#########################################################################################################################################################

# Captain's Log: Stardate 2024. 
# Objective: Establish secure and efficient communication channels between Magaluloja1 and the Distribution Center (CDD).
# Utilizing RabbitMQ for intercommunication and data exchange.

# Initialize communication relays (vhosts) for different sectors
rabbitmqctl add_vhost magaluloja1
rabbitmqctl add_vhost cdd

# Grant communication clearance to Magaluloja1 staff
rabbitmqctl set_permissions -p "magaluloja1" "accessadmin" ".*" ".*" ".*"
rabbitmqctl set_permissions -p "cdd" "accessadmin" ".*" ".*" ".*"

# Function to add user only if it does not exist
add_user_if_not_exists() {
    local username="$1"
    local password="$2"

    if ! rabbitmqctl list_users | grep -q "$username"; then
        rabbitmqctl add_user "$username" "$password"
    else
        echo "User \"$username\" already exists, skipping creation."
    fi
}

# Register staff with access clearance
add_user_if_not_exists 'manager_magaluloja' 'SecurePass123!'
add_user_if_not_exists 'operator_cdd' 'SecurePass456!'

# Enable monitoring and admin access for the manager and operator
rabbitmqctl set_user_tags 'manager_magaluloja' 'administrator'
rabbitmqctl set_user_tags 'operator_cdd' 'monitoring'

#########################################################################################################################################################
# Configuration for Magaluloja1                                                                                                                      #
#########################################################################################################################################################

# Setting up Magaluloja1's communication exchange systems for product updates

# e.magalo.product.update - Exchange for product updates (write access for manager)
rabbitmqadmin --username=accessadmin --password=35lkK69gwoF0hGBb declare exchange --vhost=magaluloja1 name=e.magalo.product.update type=direct

# e.magalo.order.create - Exchange to create new orders (write access for operator)
rabbitmqadmin --username=accessadmin --password=35lkK69gwoF0hGBb declare exchange --vhost=magaluloja1 name=e.magalo.order.create type=direct

# e.order.create.dlq - Exchange for storing failed order data (write access for manager)
rabbitmqadmin --username=accessadmin --password=35lkK69gwoF0hGBb declare exchange --vhost=magaluloja1 name=e.order.create.dlq type=direct

# Setting up secure communication queues

# q.magalo.product.update - Queue to receive updates on products (readable by operator)
rabbitmqadmin --username=accessadmin --password=35lkK69gwoF0hGBb declare queue --vhost=magaluloja1 name=q.magalo.product.update durable=true

# q.magalo.order.create - Queue to receive new order requests (readable by manager)
rabbitmqadmin --username=accessadmin --password=35lkK69gwoF0hGBb declare queue --vhost=magaluloja1 name=q.magalo.order.create durable=true

# q.order.create.dlq - Queue to store failed orders (readable by manager)
rabbitmqadmin --username=accessadmin --password=35lkK69gwoF0hGBb declare queue --vhost=magaluloja1 name=q.order.create.dlq durable=true

# Establishing message routing protocols (bindings)

# Route 'product.update' messages from CDD to Magaluloja1
rabbitmqadmin --username=accessadmin --password=35lkK69gwoF0hGBb declare binding --vhost=magaluloja1 source="e.magalo.product.update" destination_type="queue" destination="q.magalo.product.update"

# Route 'order.create' messages from Magaluloja1 to CDD
rabbitmqadmin --username=accessadmin --password=35lkK69gwoF0hGBb declare binding --vhost=magaluloja1 source="e.magalo.order.create" destination_type="queue" destination="q.magalo.order.create"

# Route order failures (DLQ) from CDD to Magaluloja1's emergency systems
rabbitmqadmin --username=accessadmin --password=35lkK69gwoF0hGBb declare binding --vhost=magaluloja1 source="e.order.create.dlq" destination_type="queue" destination="q.order.create.dlq"

# Assign specific permissions to ensure secure communication between sectors
rabbitmqctl set_permissions -p magaluloja1 'manager_magaluloja' '' 'e.magalo.order.create' 'q.magalo.product.update'
rabbitmqctl set_permissions -p magaluloja1 'operator_cdd' '' 'e.magalo.product.update|e.order.create.dlq' 'q.magalo.order.create|q.order.create.dlq'

#########################################################################################################################################################
# Configuration for Distribution Center (CDD)                                                                                                         #
#########################################################################################################################################################

# Setting up CDD's communication systems to sync with Magaluloja1

# e.magalo.product.update - Exchange for product updates (writable by operator)
rabbitmqadmin --username=accessadmin --password=35lkK69gwoF0hGBb declare exchange --vhost=cdd name=e.magalo.product.update type=direct

# e.magalo.order.create - Exchange for creating new orders (writable by manager)
rabbitmqadmin --username=accessadmin --password=35lkK69gwoF0hGBb declare exchange --vhost=cdd name=e.magalo.order.create type=direct

# e.order.create.dlq - Exchange to store failed orders (writable by manager)
rabbitmqadmin --username=accessadmin --password=35lkK69gwoF0hGBb declare exchange --vhost=cdd name=e.order.create.dlq type=direct

# Create corresponding queues for each exchange
rabbitmqadmin --username=accessadmin --password=35lkK69gwoF0hGBb declare queue --vhost=cdd name=q.magalo.product.update durable=true
rabbitmqadmin --username=accessadmin --password=35lkK69gwoF0hGBb declare queue --vhost=cdd name=q.magalo.order.create durable=true
rabbitmqadmin --username=accessadmin --password=35lkK69gwoF0hGBb declare queue --vhost=cdd name=q.order.create.dlq durable=true

# Binding for message routing between CDD and Magaluloja1
rabbitmqadmin --username=accessadmin --password=35lkK69gwoF0hGBb declare binding --vhost=cdd source="e.magalo.product.update" destination_type="queue" destination="q.magalo.product.update"
rabbitmqadmin --username=accessadmin --password=35lkK69gwoF0hGBb declare binding --vhost=cdd source="e.magalo.order.create" destination_type="queue" destination="q.magalo.order.create"
rabbitmqadmin --username=accessadmin --password=35lkK69gwoF0hGBb declare binding --vhost=cdd source="e.order.create.dlq" destination_type="queue" destination="q.order.create.dlq"

# Assign secure permissions for CDD staff
rabbitmqctl set_permissions -p cdd 'manager_magaluloja' '' 'e.magalo.order.create' 'q.magalo.product.update'
rabbitmqctl set_permissions -p cdd 'operator_cdd' '' 'e.magalo.product.update|e.order.create.dlq' 'q.magalo.order.create|q.order.create.dlq'

#########################################################################################################################################################
# Mission Success                                                                                                                                        #
#########################################################################################################################################################
# Magaluloja1 and the Distribution Center (CDD) are now synced and ready to share vital data across systems.
# Communication established successfully.